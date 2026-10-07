from types import SimpleNamespace

from config.settings import Settings
from services.ai_engine import AIEngine
from services.scoring_engine import calculate_match_score


class FakeResponses:
    def create(self, **kwargs):
        assert kwargs["store"] is False
        return SimpleNamespace(output_text="Tailored AI feedback")


class FakeClient:
    responses = FakeResponses()


def test_ai_engine_uses_responses_api_when_enabled():
    settings = Settings(openai_api_key="test-key", openai_model="test-model")
    engine = AIEngine(settings, client_factory=lambda **_: FakeClient())
    analysis = calculate_match_score("Python developer", "Python developer wanted for API work")
    result = engine.feedback("Python developer", "Python developer wanted", analysis)
    assert result["source"] == "OpenAI"
    assert result["content"] == "Tailored AI feedback"


def test_ai_engine_falls_back_without_key():
    engine = AIEngine(Settings(openai_api_key=""))
    analysis = calculate_match_score("Python developer", "Python developer wanted for API work")
    result = engine.feedback("Python developer", "Python developer wanted", analysis)
    assert result["source"] == "Local analysis"
    assert result["content"]

