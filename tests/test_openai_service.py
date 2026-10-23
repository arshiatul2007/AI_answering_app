from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from app.config import settings as settings_module
from app.services.openai_service import GeminiService


def _set_valid_env(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-3.8-flash")
    monkeypatch.setenv("TEMPERATURE", "0.2")
    settings_module.get_settings.cache_clear()


def test_gemini_service_initializes_with_settings(monkeypatch):
    _set_valid_env(monkeypatch)

    with patch("app.services.openai_service.genai") as mock_genai:
        mock_client = MagicMock()
        mock_genai.Client.return_value = mock_client

        service = GeminiService()

        assert service.api_key == "test-key"
        assert service.model == "gemini-3.8-flash"
        assert service.temperature == 0.2
        mock_genai.Client.assert_called_once_with(api_key="test-key")


def test_generate_answer_returns_response_content(monkeypatch):
    _set_valid_env(monkeypatch)

    with patch("app.services.openai_service.genai") as mock_genai:
        mock_client = MagicMock()
        mock_genai.Client.return_value = mock_client
        mock_client.models.generate_content.return_value = SimpleNamespace(
            text="This is the answer."
        )

        service = GeminiService()
        answer = service.generate_answer(
            [{"role": "user", "content": "What is Python?"}],
            system_prompt="You are helpful.",
        )

        assert answer == "This is the answer."
        mock_client.models.generate_content.assert_called_once()


def test_generate_answer_handles_api_errors(monkeypatch):
    _set_valid_env(monkeypatch)

    with patch("app.services.openai_service.genai") as mock_genai:
        mock_client = MagicMock()
        mock_genai.Client.return_value = mock_client
        mock_client.models.generate_content.side_effect = RuntimeError("API failed")

        service = GeminiService()

        with pytest.raises(RuntimeError, match="AI service is unavailable"):
            service.generate_answer([{"role": "user", "content": "What is Python?"}])
