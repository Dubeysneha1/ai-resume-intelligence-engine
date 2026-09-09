import re
import json
from pathlib import Path
from typing import Dict, List, Optional
from app.models.domain import ContactInfo, ExtractedSkills, ParsedResume


class ResumeExtractor:
    SECTION_HEADERS = {
        "education": [r"education", r"academic", r"qualifications"],
        "experience": [r"experience", r"employment history", r"work experience", r"internships?"],
        "projects": [r"projects?", r"academic projects?", r"personal projects?"],
        "skills": [r"skills?", r"technical skills?", r"core competencies", r"technologies"],
        "certifications": [r"certifications?", r"licenses?", r"courses"]
    }

    def __init__(self, taxonomy_path: Optional[str] = None):
        if taxonomy_path is None:
            # Default to backend/data/skills_taxonomy.json
            taxonomy_path = Path(__file__).resolve().parents[3] / "data" / "skills_taxonomy.json"
        
        with open(taxonomy_path, "r", encoding="utf-8") as f:
            self.taxonomy = json.load(f)

    def extract_contact_info(self, text: str) -> ContactInfo:
        # Standard RFC-compliant email pattern
        email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
        emails = re.findall(email_pattern, text)
        
        # Matches common international and domestic phone formats (+91, standard 10 digits, etc.)
        phone_pattern = r"(?:(?:\+|0{0,2})91[\s-]?)?[6789]\d{9}|(?:\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}"
        phones = re.findall(phone_pattern, text)

        # Common developer profile URLs
        url_pattern = r"(?:https?:\/\/)?(?:www\.)?(?:linkedin\.com\/in\/[a-zA-Z0-9_-]+|github\.com\/[a-zA-Z0-9_-]+)"
        links = re.findall(url_pattern, text, re.IGNORECASE)

        # Simple name heuristic: inspect the very first non-empty lines before contact details
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        candidate_name = lines[0] if lines else None
        if candidate_name and len(candidate_name.split()) > 4:
            # If line is too long, it's likely a header or sentence, not a pure name
            candidate_name = None

        return ContactInfo(
            name=candidate_name,
            email=emails[0] if emails else None,
            phone=phones[0] if phones else None,
            links=list(set(links))
        )

    def extract_skills(self, text: str) -> ExtractedSkills:
        text_lower = text.lower()
        extracted: Dict[str, List[str]] = {
            "languages": [],
            "frameworks": [],
            "ai_ml": [],
            "tools": []
        }
        all_skills = []

        mapping = {
            "languages": "languages",
            "frameworks_and_libraries": "frameworks",
            "ai_ml_concepts": "ai_ml",
            "tools_and_platforms": "tools"
        }

        for tax_key, target_key in mapping.items():
            for skill in self.taxonomy.get(tax_key, []):
                # Escaping skill names for regex (handles symbols like c++, .js)
                pattern = r"\b" + re.escape(skill) + r"\b"
                if re.search(pattern, text_lower):
                    extracted[target_key].append(skill)
                    all_skills.append(skill)

        return ExtractedSkills(
            languages=sorted(set(extracted["languages"])),
            frameworks=sorted(set(extracted["frameworks"])),
            ai_ml=sorted(set(extracted["ai_ml"])),
            tools=sorted(set(extracted["tools"])),
            all_skills=sorted(set(all_skills))
        )

    def segment_sections(self, text: str) -> Dict[str, str]:
        lines = text.splitlines()
        sections: Dict[str, List[str]] = {}
        current_section = "summary"
        sections[current_section] = []

        # Build regex map for headers
        compiled_headers = {}
        for sec_name, variations in self.SECTION_HEADERS.items():
            pattern = r"^\s*(?:" + "|".join(variations) + r")\s*[:\-]?\s*$"
            compiled_headers[sec_name] = re.compile(pattern, re.IGNORECASE)

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            # Check if this line signals a new section header
            matched_section = None
            for sec_name, regex in compiled_headers.items():
                if regex.match(stripped):
                    matched_section = sec_name
                    break

            if matched_section:
                current_section = matched_section
                if current_section not in sections:
                    sections[current_section] = []
            else:
                sections[current_section].append(stripped)

        return {k: "\n".join(v).strip() for k, v in sections.items() if v}

    def parse(self, raw_text: str) -> ParsedResume:
        return ParsedResume(
            contact=self.extract_contact_info(raw_text),
            skills=self.extract_skills(raw_text),
            sections=self.segment_sections(raw_text),
            raw_text=raw_text
        )