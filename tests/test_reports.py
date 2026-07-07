def test_weekly_report_draft_uses_daily_report_and_ledgers(client):
    client.post(
        "/api/daily-reports",
        json={
            "report_date": "2026-07-07",
            "owner": "张旭",
            "planned_items": "拜访北京示例科技有限公司",
            "completed_items": "完成客户拜访并形成资金申报商机",
            "unfinished_reason": "",
            "new_visits": 1,
            "new_channels": 0,
            "project_progress": "绿色低碳改造项目进入需求沟通",
            "contract_payment_progress": "待确认付款节点",
            "tomorrow_plan": "提交资料清单",
            "support_needed": "需技术确认申报条件",
        },
    )

    response = client.post(
        "/api/reports/weekly/draft",
        json={
            "period_start": "2026-07-06",
            "period_end": "2026-07-12",
            "owner": "张旭",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["report_type"] == "weekly"
    assert "完成客户拜访" in payload["content"]
    assert "需技术确认申报条件" in payload["content"]


def test_monthly_review_draft_works_without_ai_key(client):
    response = client.post(
        "/api/reports/monthly-review/draft",
        json={
            "month": "2026-07",
            "owner": "公司",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["report_type"] == "monthly_review"
    assert "目标完成情况" in payload["content"]
    assert payload["ai_enhanced"] is False
