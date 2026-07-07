from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Settings:
    project_name: str = "北京公司经营管理 AI Agent"
    database_url: str = f"sqlite+pysqlite:///{PROJECT_ROOT / 'data' / 'degu_oa.sqlite3'}"
    host: str = "127.0.0.1"
    port: int = 8766
    ai_base_url: str = ""
    ai_model: str = ""
    ai_api_key: str = ""


def load_settings(database_url: str | None = None) -> Settings:
    local_settings = _read_local_settings()
    return Settings(
        database_url=database_url
        or os.getenv("DATABASE_URL")
        or local_settings.get("database_url")
        or Settings.database_url,
        host=os.getenv("APP_HOST") or local_settings.get("host") or Settings.host,
        port=int(os.getenv("APP_PORT") or local_settings.get("port") or Settings.port),
        ai_base_url=os.getenv("AI_BASE_URL") or local_settings.get("ai_base_url", ""),
        ai_model=os.getenv("AI_MODEL") or local_settings.get("ai_model", ""),
        ai_api_key=os.getenv("AI_API_KEY") or local_settings.get("ai_api_key", ""),
    )


def _read_local_settings() -> dict[str, str]:
    path = PROJECT_ROOT / "data" / "local_settings.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))
