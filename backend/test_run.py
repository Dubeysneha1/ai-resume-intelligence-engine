from app.services.parser.pdf_loader import PDFLoader
from app.services.parser.cleaner import TextCleaner
from app.services.nlp.extractor import ResumeExtractor

pdf_path = "sample.pdf"

try:
    with open(pdf_path, "rb") as f:
        raw_bytes = f.read()

    cleaned = TextCleaner.clean(PDFLoader.extract_text_from_bytes(raw_bytes))
    extractor = ResumeExtractor()
    parsed = extractor.parse(cleaned)

    print("=== EXTRACTED CONTACT INFO ===")
    print(parsed.contact.model_dump_json(indent=2))

    print("\n=== EXTRACTED SKILLS ===")
    print(parsed.skills.model_dump_json(indent=2))

    print("\n=== DETECTED SECTIONS ===")
    for sec_name in parsed.sections.keys():
        print(f"- {sec_name.upper()} ({len(parsed.sections[sec_name])} chars)")

    print("\n[SUCCESS] Information extraction completed.")
except FileNotFoundError:
    print(f"Place a sample PDF named '{pdf_path}' in the backend folder to test.")

    from app.services.parser.pdf_loader import PDFLoader
from app.services.parser.cleaner import TextCleaner
from app.services.nlp.extractor import ResumeExtractor
from app.services.nlp.scorer import ATSScorer
from app.models.domain import ParsedJobDescription

pdf_path = "sample.pdf"

sample_jd = """
We are looking for an AI Engineer with strong Python and Machine Learning skills. 
The candidate should have experience with FastAPI, Docker, and Natural Language Processing (NLP).
Experience with transformers, vector search, and embeddings is highly preferred.
Knowledge of AWS or cloud platforms is a plus.
"""

try:
    with open(pdf_path, "rb") as f:
        raw_bytes = f.read()

    cleaned_resume = TextCleaner.clean(PDFLoader.extract_text_from_bytes(raw_bytes))
    extractor = ResumeExtractor()

    # Parse resume
    parsed_resume = extractor.parse(cleaned_resume)

    # Parse Job Description
    parsed_jd = ParsedJobDescription(
        raw_text=sample_jd,
        required_skills=extractor.extract_skills(sample_jd)
    )

    # Run ATS Matcher
    scorer = ATSScorer()
    results = scorer.calculate_match(parsed_resume, parsed_jd)

    print("=== HYBRID ATS MATCH RESULTS ===")
    print(f"Overall ATS Score  : {results.ats_score}%")
    print(f"Skill Match Score  : {results.skill_score}%")
    print(f"Semantic Similarity: {results.semantic_score}%")
    print(f"Matching Skills    : {', '.join(results.matching_skills) if results.matching_skills else 'None'}")
    print(f"Missing Skills     : {', '.join(results.missing_skills) if results.missing_skills else 'None'}")
    print("\n[SUCCESS] Scoring engine verified.")
except FileNotFoundError:
    print(f"Place a sample PDF named '{pdf_path}' in the backend folder to test.")