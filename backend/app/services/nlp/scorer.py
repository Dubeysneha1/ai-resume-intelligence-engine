import numpy as np
from typing import List, Set
from app.models.domain import ParsedResume, ParsedJobDescription, MatchResult
from app.services.nlp.embeddings import EmbeddingEngine


class ATSScorer:
    def __init__(self, skill_weight: float = 0.60, semantic_weight: float = 0.40):
        self.skill_weight = skill_weight
        self.semantic_weight = semantic_weight
        self.embedding_engine = EmbeddingEngine()

    def _compute_semantic_similarity(self, resume_text: str, jd_text: str) -> float:
        """
        Calculates cosine similarity between resume and JD vector representations.
        Returns a percentage value between 0.0 and 100.0.
        """
        vectors = self.embedding_engine.encode([resume_text, jd_text])
        resume_vec = vectors[0]
        jd_vec = vectors[1]

        # Dot product of unit-normalized vectors equals cosine similarity
        cosine_sim = float(np.dot(resume_vec, jd_vec))
        # Clamp between 0.0 and 1.0 in case of minor floating-point artifacts
        cosine_sim = max(0.0, min(1.0, cosine_sim))
        
        return round(cosine_sim * 100, 2)

    def calculate_match(self, resume: ParsedResume, jd: ParsedJobDescription) -> MatchResult:
        resume_skills_set: Set[str] = set(skill.lower() for skill in resume.skills.all_skills)
        jd_skills_set: Set[str] = set(skill.lower() for skill in jd.required_skills.all_skills)

        # 1. Skill overlap calculation
        if jd_skills_set:
            matching_skills = sorted(list(resume_skills_set.intersection(jd_skills_set)))
            missing_skills = sorted(list(jd_skills_set.difference(resume_skills_set)))
            skill_score = round((len(matching_skills) / len(jd_skills_set)) * 100, 2)
        else:
            # Fallback if JD doesn't list recognized taxonomy skills
            matching_skills = []
            missing_skills = []
            skill_score = 70.0  # Neutral baseline

        # 2. Semantic vector similarity
        semantic_score = self._compute_semantic_similarity(resume.raw_text, jd.raw_text)

        # 3. Hybrid ATS composite score
        overall_score = round(
            (skill_score * self.skill_weight) + (semantic_score * self.semantic_weight), 
            2
        )

        return MatchResult(
            ats_score=overall_score,
            skill_score=skill_score,
            semantic_score=semantic_score,
            matching_skills=matching_skills,
            missing_skills=missing_skills
        )