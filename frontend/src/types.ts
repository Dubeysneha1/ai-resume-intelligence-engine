export interface ContactInfo {
  name?: string;
  email?: string;
  phone?: string;
  linkedin?: string;
  github?: string;
}

export interface ExtractedSkills {
  technical: string[];
  soft: string[];
  all_extracted_skills: string[];
}

export interface ScoreBreakdown {
  keyword_score: number;
  semantic_score: number;
  total_score: number;
}

export interface InterviewQuestions {
  technical: string[];
  project_based: string[];
  behavioral: string[];
}

export interface AIAnalysisReport {
  summary: string;
  strengths: string[];
  weaknesses: string[];
  actionable_suggestions: string[];
  interview_questions: InterviewQuestions;
}

export interface AnalysisResponse {
  filename: string;
  contact_info: ContactInfo;
  skills: ExtractedSkills;
  matching_skills: string[];
  missing_skills: string[];
  scores: ScoreBreakdown;
  ai_report: AIAnalysisReport;
}