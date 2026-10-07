"""Environment-backed settings for the application."""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    app_name: str = "AI Resume Analyzer"
    app_tagline: str = "Turn your resume into a stronger match."
    openai_api_key: str = ""
    openai_model: str = "gpt-5-mini"
    max_file_size_mb: int = 10
    app_env: str = "development"
    base_dir: Path = BASE_DIR

    @property
    def ai_enabled(self) -> bool:
        return bool(self.openai_api_key.strip())


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached settings object populated from environment variables."""
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", "").strip(),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-5-mini").strip() or "gpt-5-mini",
        max_file_size_mb=int(os.getenv("MAX_FILE_SIZE_MB", "10")),
        app_env=os.getenv("APP_ENV", "development").strip(),
    )

