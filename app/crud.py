from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.database import session_dependency
from app.models import (
    AuditLog,
    Channel,
    Contract,
    Customer,
    DailyReport,
    DeliveryProject,
    FieldOption,
    GeneratedReport,
    GroupProject,
    Opportunity,
    Payment,
    Plan,
    Receivable,
    User,
    Visit,
)
from app.services.audit_log import write_audit_log


RESOURCE_MODELS = {
    "customers": Customer,
    "channels": Channel,
    "visits": Visit,
    "opportunities": Opportunity,
    "group-projects": GroupProject,
    "contracts": Contract,
    "receivables": Receivable,
    "payments": Payment,
    "delivery-projects": DeliveryProject,
    "plans": Plan,
    "daily-reports": DailyReport,
    "generated-reports": GeneratedReport,
    "users": User,
    "settings/options": FieldOption,
}


def build_crud_router(session_factory) -> APIRouter:
    router = APIRouter(prefix="/api")
    get_session = session_dependency(session_factory)

    for resource_name, model in RESOURCE_MODELS.items():
        _register_resource(router, resource_name, model, get_session)

    @router.get("/audit-logs")
    def list_audit_logs(session: Session = Depends(get_session)) -> list[dict[str, Any]]:
        logs = session.scalars(select(AuditLog).order_by(AuditLog.id.desc())).all()
        return [to_dict(log) for log in logs]

    return router


def _register_resource(router: APIRouter, resource_name: str, model: type, get_session) -> None:
    path = f"/{resource_name}"

    @router.get(path, name=f"list_{resource_name}")
    def list_records(session: Session = Depends(get_session), _model: type = model) -> list[dict[str, Any]]:
        statement: Select = select(_model).order_by(_model.id.desc())
        records = session.scalars(statement).all()
        return [to_dict(record) for record in records]

    @router.post(path, name=f"create_{resource_name}")
    def create_record(
        payload: dict[str, Any],
        session: Session = Depends(get_session),
        _model: type = model,
        _resource_name: str = resource_name,
    ) -> dict[str, Any]:
        values = coerce_payload(_model, payload)
        record = _model(**values)
        session.add(record)
        session.flush()
        write_audit_log(
            session,
            entity_type=_resource_name,
            entity_id=record.id,
            action="create",
            summary=f"创建{_resource_name}记录",
        )
        session.commit()
        session.refresh(record)
        return to_dict(record)

    @router.patch(f"{path}/{{record_id}}", name=f"update_{resource_name}")
    def update_record(
        record_id: int,
        payload: dict[str, Any],
        session: Session = Depends(get_session),
        _model: type = model,
        _resource_name: str = resource_name,
    ) -> dict[str, Any]:
        record = session.get(_model, record_id)
        if record is None:
            raise HTTPException(status_code=404, detail=f"{_resource_name} record not found")
        for key, value in coerce_payload(_model, payload).items():
            setattr(record, key, value)
        write_audit_log(
            session,
            entity_type=_resource_name,
            entity_id=record.id,
            action="update",
            summary=f"更新{_resource_name}记录",
        )
        session.commit()
        session.refresh(record)
        return to_dict(record)


def coerce_payload(model: type, payload: dict[str, Any]) -> dict[str, Any]:
    values: dict[str, Any] = {}
    columns = model.__table__.columns
    for key, value in payload.items():
        if key not in columns or key in {"id", "created_at", "updated_at"}:
            continue
        column = columns[key]
        python_type = getattr(column.type, "python_type", None)
        if value == "":
            values[key] = None if column.nullable and python_type is date else ""
        elif python_type is date and isinstance(value, str):
            values[key] = date.fromisoformat(value)
        elif python_type is Decimal:
            values[key] = Decimal(str(value or 0))
        else:
            values[key] = value
    return values


def to_dict(record: Any) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for column in record.__table__.columns:
        value = getattr(record, column.name)
        if isinstance(value, Decimal):
            value = float(value)
        elif isinstance(value, (date, datetime)):
            value = value.isoformat()
        result[column.name] = value
    return result
