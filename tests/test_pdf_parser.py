from io import BytesIO

import pytest

from services.pdf_parser import ResumeParseError, extract_resume_text


def test_extract_txt_resume():
    source = BytesIO(b"Jane Doe\nPython Developer\nSkills: Python, SQL")
    assert "Python Developer" in extract_resume_text(source, "resume.txt")


def test_rejects_unknown_format():
    with pytest.raises(ResumeParseError):
        extract_resume_text(b"data", "resume.rtf")


def test_txt_requires_utf8():
    with pytest.raises(ResumeParseError):
        extract_resume_text(b"\xff\xfe\xfa", "resume.txt")

