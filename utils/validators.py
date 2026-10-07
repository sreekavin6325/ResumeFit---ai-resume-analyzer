"""Input validation helpers."""

from __future__ import annotations

from pathlib import Path

from utils.constants import ALLOWED_FILE_TYPES


def validate_resume_file(uploaded_file: object, max_size_mb: int = 10) -> tuple[bool, str]:
    if uploaded_file is None:
        return False, "Please upload a resume."
    name = getattr(uploaded_file, "name", "")
    suffix = Path(name).suffix.lower().lstrip(".")
    if suffix not in ALLOWED_FILE_TYPES:
        return False, "Upload a PDF, DOCX, or TXT file."
    size = getattr(uploaded_file, "size", None)
    if size is None and hasattr(uploaded_file, "getvalue"):
        size = len(uploaded_file.getvalue())
    if size is not None and size > max_size_mb * 1024 * 1024:
        return False, f"The file exceeds the {max_size_mb} MB limit."
    return True, ""


def validate_job_description(text: str, minimum_characters: int = 80) -> tuple[bool, str]:
    if not text or not text.strip():
        return False, "Paste a job description or load a sample role."
    if len(text.strip()) < minimum_characters:
        return False, f"Use at least {minimum_characters} characters for a meaningful comparison."
    return True, ""

