import fitz  # PyMuPDF
from typing import List, Dict, Any


class PDFLoader:
    @staticmethod
    def extract_text_from_bytes(file_bytes: bytes) -> str:
        """
        Extracts plain text from raw PDF bytes while sorting blocks 
        geometrically (top-to-bottom, left-to-right) to respect multi-column resumes.
        """
        # Open the PDF directly from in-memory byte stream
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        extracted_pages: List[str] = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Extract structured blocks: (x0, y0, x1, y1, "text", block_no, block_type)
            # block_type == 0 indicates text; block_type == 1 indicates an image
            blocks = page.get_text("blocks")
            
            # Filter for text blocks only
            text_blocks = [b for b in blocks if b[6] == 0]
            
            # Sort blocks primarily by vertical position (y0), then horizontal (x0)
            # For strict multi-column resumes, y0 is often grouped by column bounds.
            # Using (round(y0, -1), x0) groups blocks within the same vertical band.
            sorted_blocks = sorted(text_blocks, key=lambda b: (b[1], b[0]))
            
            page_text = "\n".join(b[4].strip() for b in sorted_blocks if b[4].strip())
            extracted_pages.append(page_text)

        doc.close()
        return "\n\n--- Page Break ---\n\n".join(extracted_pages)