import asyncio
import json
from typing import List, Dict, Any
from fastmcp import FastMCP, Client
from fastmcp.prompts.prompt import Message

from dotenv import load_dotenv
load_dotenv()
import requests
import os
from openai import OpenAI
client = OpenAI()


# Create the FastMCP server
mcp = FastMCP(
    name="MCP Discovery Server",
    instructions="""
    This server helps you discover and find the best Model Context Protocol (MCP) servers.
    Use the search_mcps tool to find MCPs based on your requirements.
    Use the get_mcp_details tool to get detailed information about a specific MCP.
    Use the recommend_mcps tool to get personalized recommendations based on your use case.
    """
)

@mcp.tool
async def list_mcps_from_smithery(query: str, limit: int = 10) -> Dict[str, Any]:
    
    """ List the sources of MCP knowledge
    The tool will return the urls that cosnist of the mcp knowledge base"""

    url = "https://registry.smithery.ai/servers"
    querystring = {"q":query, "page":1}
    headers = {"Authorization": f"Bearer {os.getenv('SMITHERY_API_KEY')}"}
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

@mcp.tool
async def list_mcp_from_web_search(query: str, limit: int = 10) -> str:
    """
    This tool is used to list the urls of the mcp servers that are related to the query.
    """
    response = client.responses.create(
        model="gpt-4o-mini",
        tools=[{"type": "web_search_preview"}],
        input=f"List the urls of the mcp servers that are related to {query}"
    )
    return response.output_text

@mcp.resource("resource://sources", mime_type="application/json")
async def list_sources() -> str:
    """
    This resource is used to list the sources of mcp servers.
    """
    return json.dumps({
        "smithery": {"description": "The smithery mcp server"},
        "web_search": {"description": "The openai web search mcp server"}
    })

@mcp.resource("resource://{source_name}/validate_sources", mime_type="application/json")
async def validate_sources(source_name: str) -> str:
    """
    This resource is used to validate the sources of mcp servers.
    """
    source_name = source_name.lower()
    if source_name == "smithery":
        return json.dumps({"status": "success", "message": "Smithery is a trusted source of mcp servers"})
    elif source_name == "web_search":
        return json.dumps({"status": "success", "message": "The openai web search is a trusted source of mcp servers"})
    else:
        return json.dumps({"status": "caution", "message": f"The source name {source_name} might not be a valid source of mcp servers"})
    
@mcp.prompt
def prompt_for_mcp_server(query: str) -> Message:
    """
    This prompt is used to find the best MCP servers for a given query.
    """
    return Message(role="user", content=f"""
    You are a helpful assistant that helps the user find the best Model Context Protocol (MCP) servers for {query}.
    You will need to use the list_mcps_from_smithery tool to find the best MCP servers.
    You will need to use the list_mcp_from_web_search tool to find the best MCP servers.
    """)

if __name__ == "__main__":
    mcp.run()
    # mcp.run(transport="http", host="127.0.0.1", port=5000)
    


