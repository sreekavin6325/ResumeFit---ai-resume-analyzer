import pytest

from services.similarity_engine import cosine_similarity, keyword_coverage


def test_identical_text_has_full_similarity():
    assert cosine_similarity("Python SQL Docker", "Python SQL Docker") == pytest.approx(1.0)


def test_unrelated_text_has_zero_similarity():
    assert cosine_similarity("Python SQL", "Figma Illustrator") == 0.0


def test_keyword_coverage():
    ratio, matched = keyword_coverage("Built Python APIs with Docker", ["python", "sql", "docker"])
    assert ratio == pytest.approx(2 / 3)
    assert matched == ["python", "docker"]

