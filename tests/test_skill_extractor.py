from services.skill_extractor import compare_skills, extract_skills


CATALOG = {
    "languages": ["Python", "Java", "C++"],
    "ai": ["Machine Learning", "Natural Language Processing"],
    "aliases": {"NLP": "Natural Language Processing"},
}


def test_extracts_phrases_and_aliases_without_substring_false_positive():
    skills = extract_skills("Built Python NLP services; communicated results.", CATALOG)
    assert skills == ["Natural Language Processing", "Python"]
    assert "C++" not in skills


def test_compare_skills_is_case_insensitive():
    result = compare_skills(["python", "SQL"], ["Python", "Docker"])
    assert result["matched"] == ["Python"]
    assert result["missing"] == ["Docker"]
    assert result["coverage"] == 50.0

