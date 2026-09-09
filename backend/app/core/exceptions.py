from fastapi import HTTPException, status


class FileValidationException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class PDFParsingException(HTTPException):
    def __init__(self, detail: str = "Unable to process or parse the provided PDF document."):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class AIAnalysisException(HTTPException):
    def __init__(self, detail: str = "AI analysis pipeline failed to produce results."):
        super().__init__(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail)