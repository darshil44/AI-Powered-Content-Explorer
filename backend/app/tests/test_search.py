import pytest
from app.schemas import search as search_schemas

@pytest.mark.asyncio
async def test_search_endpoint(client, redis_mock, monkeypatch):

    async def mock_call_tool(tool_name, params):
        return {"result": {"items": ["result1", "result2"]}}

    monkeypatch.setattr("app.mcp.client.MCPClient.call_tool", mock_call_tool)

    data = {"query": "quantum computing"}
    res = await client.post("/api/v1/search/", json=data)
    assert res.status_code == 200
    assert res.json()["cached"] is False
    assert "result" in res.json()

    # Second call should be cached
    res = await client.post("/api/v1/search/", json=data)
    assert res.status_code == 200
    assert res.json()["cached"] is True