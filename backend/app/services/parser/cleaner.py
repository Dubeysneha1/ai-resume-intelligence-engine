import re
import unicodedata


class TextCleaner:
    LIGATURES = {
        "ﬁ": "fi",
        "ﬂ": "fl",
        "ﬀ": "ff",
        "ﬃ": "ffi",
        "ﬄ": "ffl",
    }

    @classmethod
    def clean(cls, text: str) -> str:
        """
        Normalizes extracted PDF text into clean, searchable, tokenizable prose.
        """
        if not text:
            return ""

        # Normalize unicode characters
        text = unicodedata.normalize("NFKD", text)

        # Fix ligatures
        for ligature, replacement in cls.LIGATURES.items():
            text = text.replace(ligature, replacement)

        # Replace bullet points with standard hyphens
        text = re.sub(r"[\u2022\u2023\u25E6\u2043\u2219]", "-", text)

        # Remove unprintable/control characters
        text = re.sub(r"[^\x20-\x7E\n\t]", " ", text)

        # Collapse excessive whitespace
        text = re.sub(r"[ \t]+", " ", text)

        # Normalize newlines
        text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)

        return text.strip()