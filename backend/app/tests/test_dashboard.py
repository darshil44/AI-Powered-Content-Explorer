import pytest

@pytest.mark.asyncio
async def test_dashboard_crud(client, monkeypatch):
    # Mock MCP for initial data generation

    async def mock_search_tool(tool_name, params):
        return {"result": {"items": ["search1"]}}

    async def mock_image_tool(tool_name, params):
        return {"result": {"url": "http://image.url/test.png"}}

    monkeypatch.setattr("app.mcp.client.MCPClient.call_tool", mock_search_tool)

    user_data = {"email": "dashuser@example.com", "password": "StrongPass1"}
    await client.post("/api/v1/auth/register", json=user_data)
    login_resp = await client.post("/api/v1/auth/login", json=user_data)
    cookies = login_resp.cookies

    # Add search entry
    search_payload = {"query": "test dashboard"}
    res = await client.post("/api/v1/search/", json=search_payload, cookies=cookies)
    assert res.status_code == 200

    # Add image entry
    monkeypatch.setattr("app.mcp.client.MCPClient.call_tool", mock_image_tool)
    image_payload = {"prompt": "test prompt"}
    res = await client.post("/api/v1/image/", json=image_payload, cookies=cookies)
    assert res.status_code == 201

    # Get dashboard entries
    res = await client.get("/api/v1/dashboard/", cookies=cookies)
    assert res.status_code == 200
    json_res = res.json()
    assert "searches" in json_res
    assert "images" in json_res

    # Delete search entry
    if json_res["searches"]:
        search_id = json_res["searches"][0]["id"]
        res = await client.delete(f"/api/v1/dashboard/search/{search_id}", cookies=cookies)
        assert res.status_code == 204

    # Delete image entry
    if json_res["images"]:
        image_id = json_res["images"][0]["id"]
        res = await client.delete(f"/api/v1/dashboard/image/{image_id}", cookies=cookies)
        assert res.status_code == 204