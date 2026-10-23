from __future__ import annotations

import pytest

from app.config import settings as settings_module


def test_settings_loads_from_environment(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-3.8-flash")
    monkeypatch.setenv("TEMPERATURE", "0.5")
    settings_module.get_settings.cache_clear()

    settings = settings_module.get_settings()

    assert settings.gemini_api_key == "test-key"
    assert settings.gemini_model == "gemini-3.8-flash"
    assert settings.temperature == 0.5


def test_missing_api_key_raises_value_error(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    settings_module.get_settings.cache_clear()

    with pytest.raises(ValueError, match="GEMINI_API_KEY is missing"):
        settings_module.get_settings()


def test_invalid_temperature_raises_value_error(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setenv("TEMPERATURE", "not-a-number")
    settings_module.get_settings.cache_clear()

    with pytest.raises(ValueError, match="TEMPERATURE must be a valid float value"):
        settings_module.get_settings()
