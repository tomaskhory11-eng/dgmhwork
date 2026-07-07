from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import Settings, load_settings
from app.crud import build_crud_router
from app.database import init_db, make_engine, make_session_factory
from app.routers.dashboard import build_dashboard_router
from app.routers.reports import build_reports_router
from app.routers.workflows import build_workflow_router
from app.seed import seed_defaults


def create_app(database_url: str | None = None) -> FastAPI:
    settings = load_settings(database_url)
    engine = make_engine(settings.database_url)
    session_factory = make_session_factory(engine)
    init_db(engine)
    with session_factory() as session:
        seed_defaults(session)

    app = FastAPI(title=settings.project_name)
    app.state.settings = settings
    app.state.engine = engine
    app.state.session_factory = session_factory

    static_dir = Path(__file__).resolve().parents[1] / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": settings.project_name}

    @app.get("/")
    def index() -> FileResponse:
        return FileResponse(static_dir / "index.html")

    app.include_router(build_dashboard_router(session_factory))
    app.include_router(build_workflow_router(session_factory))
    app.include_router(build_reports_router(session_factory))
    app.include_router(build_crud_router(session_factory))

    return app


app = create_app()
