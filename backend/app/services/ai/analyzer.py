import json
import re
from openai import OpenAI
from app.core.config import settings
from app.models.domain import AIAnalysisReport, InterviewQuestions
from app.services.ai.prompts import SYSTEM_INSTRUCTION, generate_analysis_prompt


class AIAnalyzerService:
    def __init__(self):
        api_key = settings.GROK_API_KEY or "dummy-key"
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.x.ai/v1",
            timeout=10.0,
        )
        self.model_name = "grok-beta"

    def generate_report(
        self,
        resume_text: str,
        jd_text: str,
        matching_skills: list[str],
        missing_skills: list[str],
        ats_score: float,
    ) -> AIAnalysisReport:
        try:
            prompt = generate_analysis_prompt(
                resume_text=resume_text,
                jd_text=jd_text,
                matching_skills=matching_skills,
                missing_skills=missing_skills,
                ats_score=ats_score,
            )

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_INSTRUCTION},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
            )

            raw_content = response.choices[0].message.content.strip()
            raw_content = re.sub(r"^```(?:json)?\s*", "", raw_content)
            raw_content = re.sub(r"\s*```$", "", raw_content)

            parsed = json.loads(raw_content)
            return AIAnalysisReport(**parsed)
        except Exception:
            # Resilient fallback using extracted NLP metadata
            return self._fallback_report(matching_skills, missing_skills, ats_score)

    def _fallback_report(
        self, matching_skills: list[str], missing_skills: list[str], ats_score: float
    ) -> AIAnalysisReport:
        strengths = [
            f"Demonstrated core competency in: {', '.join(matching_skills[:4])}."
            if matching_skills
            else "Solid baseline profile with relevant transferable foundations."
        ]
        if ats_score >= 60:
            strengths.append("High contextual overlap with target role expectations.")

        weaknesses = []
        if missing_skills:
            weaknesses.append(f"Gaps identified in required stack: {', '.join(missing_skills[:4])}.")
        else:
            weaknesses.append("Consider expanding on quantitative project impact metrics.")

        suggestions = [
            f"Integrate hands-on evidence for missing keywords ({', '.join(missing_skills[:3])})."
            if missing_skills
            else "Highlight specific architectural decisions and production trade-offs.",
            "Incorporate measurable outcomes (e.g., latency reduction, accuracy gains, scale).",
        ]

        tech_q = (
            [f"How have you applied {skill} in a production environment?" for skill in matching_skills[:2]]
            if matching_skills
            else ["Can you elaborate on your primary backend technology stack?"]
        )

        return AIAnalysisReport(
            summary=(
                f"Candidate ATS match is evaluated at {ats_score}/100. "
                f"Matches {len(matching_skills)} required competencies, with {len(missing_skills)} identified development areas."
            ),
            strengths=strengths,
            weaknesses=weaknesses,
            actionable_suggestions=suggestions,
            interview_questions=InterviewQuestions(
                technical=tech_q,
                project_based=[
                    "Walk through the architecture and data flow of your most technically complex project.",
                    "Describe a critical failure or bottleneck you encountered and how you mitigated it.",
                ],
                behavioral=[
                    "How do you manage deadlines and ambiguous specifications in fast-paced development cycles?",
                ],
            ),
        )