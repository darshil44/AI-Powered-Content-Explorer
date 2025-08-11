import uuid
import httpx

class MCPClient:
    def __init__(self, base_url: str, api_key: str | None = None, timeout: int = 30):
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout

    async def call_tool(self, tool_name: str, arguments: dict):
        payload = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            # many hosted MCPs accept Bearer in Authorization. adapt in config if needed.
            headers["Authorization"] = f"Bearer {self.api_key}"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(self.base_url, json=payload, headers=headers)
            resp.raise_for_status()
            return resp.json()
