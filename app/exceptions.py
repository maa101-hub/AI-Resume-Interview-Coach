"""Custom exception classes for the AI Resume & Interview Coach application."""


class FileFormatError(Exception):
    """Raised when an uploaded file is not in a supported format (PDF or DOCX)."""

    def __init__(self, message: str = "Unsupported file format. Please upload a PDF or DOCX file."):
        self.message = message
        super().__init__(self.message)


class EmptyFileError(Exception):
    """Raised when an uploaded file is empty or contains no extractable text."""

    def __init__(self, message: str = "The uploaded file is empty or contains no extractable text."):
        self.message = message
        super().__init__(self.message)


class FileSizeError(Exception):
    """Raised when an uploaded file exceeds the maximum allowed size of 5MB."""

    def __init__(self, message: str = "File exceeds the maximum size of 5MB."):
        self.message = message
        super().__init__(self.message)


class ScoringError(Exception):
    """Raised when the ATS scorer fails to complete scoring."""

    def __init__(self, message: str = "Unable to complete scoring. Please try again."):
        self.message = message
        super().__init__(self.message)


class InsufficientContentError(Exception):
    """Raised when resume content is insufficient for analysis."""

    def __init__(self, message: str = "Resume content is insufficient for analysis. Please verify your uploaded file."):
        self.message = message
        super().__init__(self.message)


class AIServiceError(Exception):
    """Raised when the AI service (OpenAI) fails to respond."""

    def __init__(self, message: str = "Unable to generate interview questions. Please try again later."):
        self.message = message
        super().__init__(self.message)
