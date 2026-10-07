"""Optional OpenAI-powered feedback with a reliable local fallback."""

from __future__ import annotations

from typing import Callable

from config.settings import Settings, get_settings
from prompts.interview_prompt import build_interview_prompt
from prompts.resume_analysis_prompt import build_resume_analysis_prompt
from services.recommendation_engine import generate_interview_questions, generate_recommendations


class AIEngine:
    def __init__(self, settings: Settings | None = None, client_factory: Callable | None = None):
        self.settings = settings or get_settings()
        self._client_factory = client_factory

    @property
    def enabled(self) -> bool:
        return self.settings.ai_enabled

    def _client(self):
        if self._client_factory:
            return self._client_factory(api_key=self.settings.openai_api_key)
        from openai import OpenAI

        return OpenAI(api_key=self.settings.openai_api_key)

    def _generate(self, prompt: str) -> str:
        if not self.enabled:
            raise RuntimeError("OPENAI_API_KEY is not configured.")
        response = self._client().responses.create(
            model=self.settings.openai_model,
            input=prompt,
            store=False,
        )
        return response.output_text.strip()

    def feedback(self, resume_text: str, job_description: str, analysis: dict) -> dict:
        if self.enabled:
            try:
                text = self._generate(build_resume_analysis_prompt(resume_text, job_description, analysis))
                return {"source": "OpenAI", "content": text, "error": None}
            except Exception as exc:
                error = str(exc)
        else:
            error = None
        recommendations = generate_recommendations(resume_text, analysis)
        content = "\n\n".join(
            f"### {item['title']}\n{item['detail']}" for item in recommendations
        )
        return {"source": "Local analysis", "content": content, "error": error}

    def interview_questions(self, resume_text: str, job_description: str, analysis: dict) -> dict:
        if self.enabled:
            try:
                prompt = build_interview_prompt(resume_text, job_description, analysis["skills"]["missing"])
                return {"source": "OpenAI", "content": self._generate(prompt), "error": None}
            except Exception as exc:
                error = str(exc)
        else:
            error = None
        questions = generate_interview_questions(analysis)
        content = "\n\n".join(
            f"**{index}. {item['category']}**  \n{item['question']}"
            for index, item in enumerate(questions, start=1)
        )
        return {"source": "Local analysis", "content": content, "error": error}

