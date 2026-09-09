from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class ContactInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    links: List[str] = Field(default_factory=list)


class ExtractedSkills(BaseModel):
    languages: List[str] = Field(default_factory=list)
    frameworks: List[str] = Field(default_factory=list)
    ai_ml: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    all_skills: List[str] = Field(default_factory=list)


class ParsedResume(BaseModel):
    contact: ContactInfo
    skills: ExtractedSkills
    sections: Dict[str, str] = Field(default_factory=dict)
    raw_text: str


class ParsedJobDescription(BaseModel):
    raw_text: str
    required_skills: ExtractedSkills


class MatchResult(BaseModel):
    ats_score: float
    skill_score: float
    semantic_score: float
    matching_skills: List[str]
    missing_skills: List[str]


class InterviewQuestions(BaseModel):
    technical: List[str] = Field(default_factory=list)
    project_based: List[str] = Field(default_factory=list)
    behavioral: List[str] = Field(default_factory=list)


class AIAnalysisReport(BaseModel):
    summary: str
    strengths: List[str]
    weaknesses: List[str]
    actionable_suggestions: List[str]
    interview_questions: InterviewQuestions