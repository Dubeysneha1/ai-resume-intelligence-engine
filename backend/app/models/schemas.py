from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class ContactInfoResponse(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    links: List[str] = Field(default_factory=list)


class SkillsResponse(BaseModel):
    matching_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    all_extracted_skills: List[str] = Field(default_factory=list)


class ScoreBreakdownResponse(BaseModel):
    overall_ats_score: float
    skill_match_score: float
    semantic_similarity_score: float


class InterviewQuestionsResponse(BaseModel):
    technical: List[str] = Field(default_factory=list)
    project_based: List[str] = Field(default_factory=list)
    behavioral: List[str] = Field(default_factory=list)


class AnalysisResponse(BaseModel):
    contact_info: ContactInfoResponse
    scores: ScoreBreakdownResponse
    skills: SkillsResponse
    summary: str
    strengths: List[str]
    weaknesses: List[str]
    actionable_suggestions: List[str]
    interview_questions: InterviewQuestionsResponse