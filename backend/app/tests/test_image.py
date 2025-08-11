import pytest

@pytest.mark.asyncio
async def test_image_generation(client, redis_mock, monkeypatch):

    async def mock_call_tool(tool_name, params):
        return {"result": {"url": "http://image.url/sample.png"}}

    monkeypatch.setattr("app.mcp.client.MCPClient.call_tool", mock_call_tool)

    data = {"prompt": "An astronaut riding a unicorn"}
    res = await client.post("/api/v1/image/", json=data)
    assert res.status_code == 201
    json_res = res.json()
    assert not json_res["cached"]
    assert "image_url" in json_res

    # Cached call
    res = await client.post("/api/v1/image/", json=data)
    assert res.status_code == 201
    assert res.json()["cached"]