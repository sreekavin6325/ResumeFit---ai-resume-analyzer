from services.scoring_engine import calculate_match_score


RESUME = """
SUMMARY
Python developer with 4 years of experience building APIs.
EXPERIENCE
Built FastAPI services with PostgreSQL, Docker, AWS, Git, Linux and SQL.
EDUCATION
Bachelor degree in Computer Science.
SKILLS
Python, FastAPI, PostgreSQL, Docker, AWS, Git, Linux, SQL, REST API.
PROJECTS
Created a tested backend used by 5 clients.
"""

JOB = """
Python Developer
We need 3+ years of experience. Required skills: Python, FastAPI, PostgreSQL,
Docker, Git, Linux, SQL and REST API. Bachelor's degree required.
"""


def test_well_aligned_resume_scores_highly():
    result = calculate_match_score(RESUME, JOB)
    assert 0 <= result["overall_score"] <= 100
    assert result["overall_score"] >= 75
    assert result["components"]["skills"] >= 85


def test_empty_resume_does_not_crash():
    result = calculate_match_score("", JOB)
    assert 0 <= result["overall_score"] < 50

