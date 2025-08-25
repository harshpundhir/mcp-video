# test hello.py

import asyncio
from fastmcp import Client
from pprint import pprint

client = Client("mcp_server.py")

async def call_tool(name: str):
    async with client:
        result = await client.call_tool("list_mcps_from_smithery", {"query": name})
        pprint(result)

asyncio.run(call_tool("video making"))