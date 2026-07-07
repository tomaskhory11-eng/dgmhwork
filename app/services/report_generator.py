from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud import to_dict
from app.models import DailyReport, GeneratedReport
from app.services.ai_client import enhance_text_if_configured
from app.services.audit_log import write_audit_log
from app.services.metrics import dashboard_summary


def generate_weekly_report(
    session: Session,
    *,
    period_start: date,
    period_end: date,
    owner: str,
    ai_api_key: str = "",
) -> dict:
    reports = session.scalars(
        select(DailyReport)
        .where(DailyReport.report_date >= period_start, DailyReport.report_date <= period_end)
        .where(DailyReport.owner == owner if owner != "公司" else DailyReport.owner != "")
        .order_by(DailyReport.report_date.asc())
    ).all()
    metrics = dashboard_summary(session)

    completed = "\n".join(f"- {item.report_date}: {item.completed_items}" for item in reports if item.completed_items)
    support_needed = "\n".join(f"- {item.report_date}: {item.support_needed}" for item in reports if item.support_needed)
    tomorrow_plan = "\n".join(f"- {item.report_date}: {item.tomorrow_plan}" for item in reports if item.tomorrow_plan)
    project_progress = "\n".join(f"- {item.report_date}: {item.project_progress}" for item in reports if item.project_progress)

    content = f"""# {owner}周报草稿（{period_start.isoformat()} 至 {period_end.isoformat()}）

## 本周完成工作
{completed or "- 本周暂无日报完成事项。"}

## 项目推进
{project_progress or "- 本周暂无项目推进记录。"}

## 经营数据快照
- 合同累计金额：{metrics["total_contract_amount"]:.2f}
- 回款累计金额：{metrics["total_payment_amount"]:.2f}
- 储备项目预计金额：{metrics["pipeline_estimated_amount"]:.2f}

## 需协调事项
{support_needed or "- 暂无需协调事项。"}

## 下周计划
{tomorrow_plan or "- 请结合周计划补充下周重点动作。"}
"""
    content, enhanced = enhance_text_if_configured(content, api_key=ai_api_key)
    return _store_report(
        session,
        report_type="weekly",
        title=f"{owner}周报草稿",
        content=content,
        owner=owner,
        period_start=period_start,
        period_end=period_end,
        ai_enhanced=enhanced,
    )


def generate_monthly_review(
    session: Session,
    *,
    month: str,
    owner: str,
    ai_api_key: str = "",
) -> dict:
    metrics = dashboard_summary(session)
    content = f"""# {owner}{month}月复盘草稿

## 目标完成情况
- 合同累计金额：{metrics["total_contract_amount"]:.2f}
- 回款累计金额：{metrics["total_payment_amount"]:.2f}
- 客户拜访次数：{metrics["visit_count"]}
- 渠道数量：{metrics["channel_count"]}

## 项目漏斗复盘
- 储备项目预计金额：{metrics["pipeline_estimated_amount"]:.2f}
- 重点推进项目数：{metrics["key_project_count"]}

## 合同回款复盘
- 应收未收金额：{metrics["receivable_outstanding"]:.2f}
- 请结合合同台账和回款明细补充关键判断。

## 交付进度复盘
- 延期项目数：{metrics["delayed_delivery_count"]}
- 请项目负责人补充成果文件、客户确认和需协调事项。

## 下月计划
- 从未完成事项、重点项目和经营目标中形成下月计划草稿。
"""
    content, enhanced = enhance_text_if_configured(content, api_key=ai_api_key)
    return _store_report(
        session,
        report_type="monthly_review",
        title=f"{owner}{month}月复盘草稿",
        content=content,
        owner=owner,
        month=month,
        ai_enhanced=enhanced,
    )


def _store_report(
    session: Session,
    *,
    report_type: str,
    title: str,
    content: str,
    owner: str,
    ai_enhanced: bool,
    period_start: date | None = None,
    period_end: date | None = None,
    month: str = "",
) -> dict:
    report = GeneratedReport(
        report_type=report_type,
        period_start=period_start,
        period_end=period_end,
        month=month,
        owner=owner,
        title=title,
        content=content,
        ai_enhanced=ai_enhanced,
    )
    session.add(report)
    session.flush()
    write_audit_log(
        session,
        entity_type="generated-reports",
        entity_id=report.id,
        action="create",
        summary=f"生成{title}",
    )
    session.commit()
    session.refresh(report)
    return to_dict(report)
