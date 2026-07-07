from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AISettings:
    base_url: str = ""
    model: str = ""
    api_key_configured: bool = False


def public_ai_settings(base_url: str = "", model: str = "", api_key: str = "") -> dict:
    settings = AISettings(base_url=base_url, model=model, api_key_configured=bool(api_key))
    return {
        "base_url": settings.base_url,
        "model": settings.model,
        "api_key_configured": settings.api_key_configured,
    }


def enhance_text_if_configured(content: str, *, api_key: str = "") -> tuple[str, bool]:
    if not api_key:
        return content, False
    return content, False
