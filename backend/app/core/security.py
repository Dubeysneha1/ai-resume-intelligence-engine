from fastapi import UploadFile
from app.core.config import settings
from app.core.exceptions import FileValidationException


async def validate_resume_file(file: UploadFile) -> bytes:
    """
    Validates uploaded file against size limits and PDF content headers.
    Returns the raw bytes if valid.
    """
    if not file.filename:
        raise FileValidationException("Uploaded file must have a valid filename.")

    extension = file.filename.split(".")[-1].lower()
    if extension not in settings.ALLOWED_EXTENSIONS:
        raise FileValidationException(
            f"Invalid file extension: '.{extension}'. Only PDF documents are supported."
        )

    # Read byte stream into memory
    content = await file.read()
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024

    if len(content) > max_bytes:
        raise FileValidationException(
            f"File size exceeds maximum threshold of {settings.MAX_UPLOAD_SIZE_MB}MB."
        )

    # Verify standard PDF magic header bytes (%PDF)
    if not content.startswith(b"%PDF"):
        raise FileValidationException("File corrupted or invalid PDF binary structure.")

    return content
