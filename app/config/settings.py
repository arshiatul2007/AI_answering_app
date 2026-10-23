from __future__ import annotations

import os
from functools import lru_cache
from typing import Final

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    DEFAULT_GEMINI_MODEL: Final[str] = "gemini-3.8-flash"
    DEFAULT_TEMPERATURE: Final[float] = 0.2

    def __init__(self) -> None:
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.gemini_model = (
            os.getenv("GEMINI_MODEL", self.DEFAULT_GEMINI_MODEL).strip()
            or self.DEFAULT_GEMINI_MODEL
        )
        self.temperature = self._load_temperature()

    def _load_temperature(self) -> float:
        raw_value = os.getenv("TEMPERATURE", str(self.DEFAULT_TEMPERATURE)).strip()
        try:
            temperature = float(raw_value)
        except ValueError as exc:
            raise ValueError("TEMPERATURE must be a valid float value.") from exc

        if not 0 <= temperature <= 2:
            raise ValueError("TEMPERATURE must be between 0 and 2.")

        return temperature

    def validate(self) -> None:
        if not self.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. Create a .env file using .env.example before running the app."
            )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return validated application settings."""

    settings = Settings()
    settings.validate()
    return settings
