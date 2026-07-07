from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import session_dependency
from app.services.ai_client import public_ai_settings
from app.services.report_generator import generate_monthly_review, generate_weekly_report


def build_reports_router(session_factory) -> APIRouter:
    router = APIRouter(prefix="/api", tags=["reports"])
    get_session = session_dependency(session_factory)

    @router.post("/reports/weekly/draft")
    def weekly_draft(payload: dict, request: Request, session: Session = Depends(get_session)) -> dict:
        settings = request.app.state.settings
        return generate_weekly_report(
            session,
            period_start=date.fromisoformat(payload["period_start"]),
            period_end=date.fromisoformat(payload["period_end"]),
            owner=payload.get("owner", "公司"),
            ai_api_key=settings.ai_api_key,
        )

    @router.post("/reports/monthly-review/draft")
    def monthly_review_draft(payload: dict, request: Request, session: Session = Depends(get_session)) -> dict:
        settings = request.app.state.settings
        return generate_monthly_review(
            session,
            month=payload["month"],
            owner=payload.get("owner", "公司"),
            ai_api_key=settings.ai_api_key,
        )

    @router.get("/settings/ai")
    def get_ai_settings(request: Request) -> dict:
        settings = request.app.state.settings
        return public_ai_settings(settings.ai_base_url, settings.ai_model, settings.ai_api_key)

    @router.post("/settings/ai")
    @router.patch("/settings/ai")
    def save_ai_settings(payload: dict, request: Request) -> dict:
        settings = request.app.state.settings
        base_url = payload.get("base_url", settings.ai_base_url)
        model = payload.get("model", settings.ai_model)
        api_key = payload.get("api_key", settings.ai_api_key)
        return public_ai_settings(base_url, model, api_key)

    return router
