"""Static values shared across analyzers and UI components."""

ALLOWED_FILE_TYPES = {"pdf", "txt", "docx"}

SCORE_WEIGHTS = {
    "skills": 0.45,
    "keywords": 0.20,
    "experience": 0.20,
    "education": 0.10,
    "completeness": 0.05,
}

RESUME_SECTIONS = {
    "summary": ("summary", "profile", "objective", "about"),
    "experience": ("experience", "employment", "work history", "professional experience"),
    "education": ("education", "academic", "qualifications"),
    "skills": ("skills", "technical skills", "competencies", "technologies"),
    "projects": ("projects", "portfolio", "selected projects"),
}

EDUCATION_LEVELS = {
    "phd": 4,
    "doctorate": 4,
    "master": 3,
    "m.tech": 3,
    "mtech": 3,
    "mba": 3,
    "bachelor": 2,
    "b.tech": 2,
    "btech": 2,
    "b.sc": 2,
    "degree": 2,
    "diploma": 1,
}

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "being", "but", "by",
    "for", "from", "had", "has", "have", "he", "her", "hers", "him", "his",
    "i", "in", "into", "is", "it", "its", "of", "on", "or", "our", "ours",
    "she", "that", "the", "their", "theirs", "them", "they", "this", "to", "was",
    "we", "were", "will", "with", "you", "your", "years", "year", "job", "role",
    "work", "working", "required", "preferred", "candidate", "responsibilities",
}

