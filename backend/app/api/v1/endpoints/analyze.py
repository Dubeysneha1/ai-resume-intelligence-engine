from fastapi import APIRouter, UploadFile, File, Form, Depends
from app.core.security import validate_resume_file
from app.core.exceptions import PDFParsingException, AIAnalysisException
from app.services.parser.pdf_loader import PDFLoader
from app.services.parser.cleaner import TextCleaner
from app.services.nlp.extractor import ResumeExtractor
from app.services.nlp.scorer import ATSScorer
from app.services.ai.analyzer import AIAnalyzerService
from app.models.domain import ParsedJobDescription
from app.models.schemas import (
    AnalysisResponse,
    ContactInfoResponse,
    SkillsResponse,
    ScoreBreakdownResponse,
    InterviewQuestionsResponse,
)

router = APIRouter()

# Instantiate core service singletons
extractor = ResumeExtractor()
scorer = ATSScorer()
ai_service = AIAnalyzerService()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    file_bytes: bytes = Depends(validate_resume_file),
):
    """
    Primary endpoint: parses PDF, calculates ATS match against target JD,
    and runs LLM reasoning to produce an actionable report.
    """
    try:
        raw_text = PDFLoader.extract_text_from_bytes(file_bytes)
        cleaned_text = TextCleaner.clean(raw_text)
        if not cleaned_text:
            raise PDFParsingException("The PDF yielded no readable text content.")
    except Exception as e:
        raise PDFParsingException(f"Error parsing document: {str(e)}")

    # 1. Parse Resume and Job Description
    parsed_resume = extractor.parse(cleaned_text)
    parsed_jd = ParsedJobDescription(
        raw_text=job_description,
        required_skills=extractor.extract_skills(job_description),
    )

    # 2. Compute Hybrid ATS Match
    match_result = scorer.calculate_match(parsed_resume, parsed_jd)

    # 3. Trigger Intelligence Layer
    try:
        ai_report = ai_service.generate_report(
            resume_text=parsed_resume.raw_text,
            jd_text=parsed_jd.raw_text,
            matching_skills=match_result.matching_skills,
            missing_skills=match_result.missing_skills,
            ats_score=match_result.ats_score,
        )
    except Exception as e:
        raise AIAnalysisException(f"Intelligence processing failed: {str(e)}")

    # 4. Construct and return typed API response
    return AnalysisResponse(
        contact_info=ContactInfoResponse(
            name=parsed_resume.contact.name,
            email=parsed_resume.contact.email,
            phone=parsed_resume.contact.phone,
            links=parsed_resume.contact.links,
        ),
        scores=ScoreBreakdownResponse(
            overall_ats_score=match_result.ats_score,
            skill_match_score=match_result.skill_score,
            semantic_similarity_score=match_result.semantic_score,
        ),
        skills=SkillsResponse(
            matching_skills=match_result.matching_skills,
            missing_skills=match_result.missing_skills,
            all_extracted_skills=parsed_resume.skills.all_skills,
        ),
        summary=ai_report.summary,
        strengths=ai_report.strengths,
        weaknesses=ai_report.weaknesses,
        actionable_suggestions=ai_report.actionable_suggestions,
        interview_questions=InterviewQuestionsResponse(
            technical=ai_report.interview_questions.technical,
            project_based=ai_report.interview_questions.project_based,
            behavioral=ai_report.interview_questions.behavioral,
        ),
    )