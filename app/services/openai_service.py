from __future__ import annotations

from typing import Sequence

try:
    from google import genai
except ImportError:  # pragma: no cover - compatibility fallback
    import google.genai as genai

from app.config.settings import get_settings
from app.utils.logging_config import get_logger

logger = get_logger(__name__)


class GeminiService:
    """Wrap Gemini API calls for question answering."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
    ) -> None:
        settings = get_settings()
        self.api_key = api_key or settings.gemini_api_key
        self.model = model or settings.gemini_model
        self.temperature = settings.temperature if temperature is None else temperature
        self.client = genai.Client(api_key=self.api_key)

    def generate_answer(
        self,
        messages: Sequence[dict[str, str]],
        system_prompt: str | None = None,
    ) -> str:
        """Generate a response based on the conversation history."""

        if not messages:
            raise ValueError("No conversation messages were provided.")

        prompt_lines: list[str] = []
        if system_prompt:
            prompt_lines.append(f"System: {system_prompt}")

        for message in messages:
            role = str(message.get("role", "")).strip()
            content = str(message.get("content", "") or "").strip()
            if role not in {"user", "assistant"}:
                continue
            if content:
                prompt_lines.append(f"{role.title()}: {content}")

        prompt = "\n".join(prompt_lines).strip()
        if not prompt:
            raise ValueError("No usable conversation content was provided.")

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={"temperature": self.temperature},
            )

            answer = getattr(response, "text", None)
            if not answer:
                return "I don't have a response for that question right now."

            return str(answer).strip()
        except Exception as exc:  # pragma: no cover - defensive catch for API errors
            logger.exception("Gemini request failed while generating an answer.")
            raise RuntimeError(
                "The AI service is unavailable right now. Please try again later."
            ) from exc


OpenAIService = GeminiService
