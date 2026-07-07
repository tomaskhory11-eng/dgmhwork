def test_visit_converts_to_opportunity(client):
    visit = client.post(
        "/api/visits",
        json={
            "visit_date": "2026-07-07",
            "customer_name": "北京示例科技有限公司",
            "visit_target": "环保负责人",
            "contact_info": "010-00000000",
            "visit_purpose": "中央环保资金项目沟通",
            "related_project": "绿色低碳改造项目",
            "business_detail": "中央环保资金申请",
            "business_owner": "张旭",
            "participants": "张旭",
            "key_notes": "客户有申报需求",
            "customer_attitude": "积极",
            "result": "形成商机",
            "estimated_amount": 800000,
            "next_action": "提交申报条件清单",
            "deadline": "2026-07-14",
            "is_opportunity": True,
        },
    ).json()

    converted = client.post(f"/api/visits/{visit['id']}/convert-to-opportunity")

    assert converted.status_code == 200
    payload = converted.json()
    assert payload["project_name"] == "绿色低碳改造项目"
    assert payload["customer_name"] == "北京示例科技有限公司"
    assert payload["estimated_contract_amount"] == 800000


def test_opportunity_converts_to_contract_then_initializes_receivable_and_delivery(client):
    opportunity = client.post(
        "/api/opportunities",
        json={
            "project_name": "绿色低碳改造项目",
            "customer_name": "北京示例科技有限公司",
            "customer_level": "A",
            "customer_category": "工业企业",
            "customer_nature": "民企",
            "province": "北京",
            "city": "北京",
            "business_segment": "中央环保资金申请",
            "business_detail": "资金申报",
            "project_source": "客户拜访",
            "project_stage": "商务谈判",
            "estimated_contract_amount": 800000,
            "expected_sign_month": "2026-08",
            "is_key_project": True,
            "business_owner": "张旭",
            "latest_follow_date": "2026-07-07",
            "follow_status": "推进中",
            "is_converted": False,
            "remark": "重点推进",
        },
    ).json()

    contract = client.post(f"/api/opportunities/{opportunity['id']}/convert-to-contract").json()
    assert contract["contract_name"] == "绿色低碳改造项目"
    assert contract["contract_amount"] == 800000

    initialized = client.post(f"/api/contracts/{contract['id']}/initialize-receivable-and-delivery")
    assert initialized.status_code == 200
    payload = initialized.json()
    assert payload["receivable"]["project_name"] == "绿色低碳改造项目"
    assert payload["delivery_project"]["project_name"] == "绿色低碳改造项目"
