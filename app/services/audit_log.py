from __future__ import annotations

from sqlalchemy.orm import Session

from app.models import AuditLog


def write_audit_log(
    session: Session,
    *,
    entity_type: str,
    entity_id: int,
    action: str,
    summary: str,
    actor: str = "system",
) -> AuditLog:
    log = AuditLog(
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        actor=actor,
        summary=summary,
    )
    session.add(log)
    return log
