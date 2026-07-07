from __future__ import annotations

from fastapi import FastAPI

from app.config import Settings, load_settings
from app.database import init_db, make_engine, make_session_factory


DEFAULT_FIELD_OPTIONS = [
    {"id": 1, "category": "project_stage", "value": "线索"},
    {"id": 2, "category": "project_stage", "value": "有效商机"},
    {"id": 3, "category": "project_stage", "value": "需求沟通"},
    {"id": 4, "category": "project_stage", "value": "方案编制"},
    {"id": 5, "category": "project_stage", "value": "商务谈判"},
    {"id": 6, "category": "project_stage", "value": "已签约"},
    {"id": 7, "category": "business_segment", "value": "中央生态环保督察整改"},
    {"id": 8, "category": "business_segment", "value": "中央环保资金申请"},
    {"id": 9, "category": "business_segment", "value": "高端环保咨询"},
    {"id": 10, "category": "business_segment", "value": "环评/验收/排污许可"},
]


def create_app(database_url: str | None = None) -> FastAPI:
    settings = load_settings(database_url)
    engine = make_engine(settings.database_url)
    session_factory = make_session_factory(engine)
    init_db(engine)

    app = FastAPI(title=settings.project_name)
    app.state.settings = settings
    app.state.engine = engine
    app.state.session_factory = session_factory

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": settings.project_name}

    @app.get("/api/settings/options")
    def settings_options() -> list[dict[str, int | str]]:
        return DEFAULT_FIELD_OPTIONS

    return app


app = create_app()
