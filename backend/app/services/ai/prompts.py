from typing import List

SYSTEM_INSTRUCTION = """
You are an expert technical recruiter and ATS evaluation engine.
Analyze the provided resume against the given job description with extreme precision.
You must return ONLY a single valid JSON object matching the requested schema without any markdown wrapping or explanation.
"""


def generate_analysis_prompt(
    resume_text: str,
    jd_text: str,
    matching_skills: List[str],
    missing_skills: List[str],
    ats_score: float,
) -> str:
    return f"""
Job Description:
\"\"\"{jd_text}\"\"\"

Extracted Resume Text:
\"\"\"{resume_text}\"\"\"

Pre-calculated ATS Score: {ats_score}/100
Matching Skills Found: {", ".join(matching_skills) if matching_skills else "None"}
Missing Skills Identified: {", ".join(missing_skills) if missing_skills else "None"}

Generate a detailed analysis adhering strictly to this JSON format:
{{
  "summary": "Concise summary of candidate match to the role",
  "strengths": ["Key strength 1", "Key strength 2"],
  "weaknesses": ["Key weakness or gap 1", "Key weakness or gap 2"],
  "actionable_suggestions": ["Concrete recommendation 1", "Concrete recommendation 2"],
  "interview_questions": {{
    "technical": ["Technical question targeting skills 1", "Technical question 2"],
    "project_based": ["Project validation question 1", "Project validation question 2"],
    "behavioral": ["Behavioral question 1", "Behavioral question 2"]
  }}
}}
"""