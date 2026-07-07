def test_health_returns_ok(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_seeded_options_are_available(client):
    response = client.get("/api/settings/options")

    assert response.status_code == 200
    payload = response.json()
    option_names = {(item["category"], item["value"]) for item in payload}
    assert ("project_stage", "需求沟通") in option_names
    assert ("business_segment", "中央环保资金申请") in option_names


def test_static_workbench_served(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "北京公司经营管理 AI Agent" in response.text
    assert "首页驾驶舱" in response.text
