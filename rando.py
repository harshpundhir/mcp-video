from openai import OpenAI
from typing import Dict, Any
client = OpenAI()


def list_mcp_from_web_search(query: str, limit: int = 10) -> Dict[str, Any]:

    response = client.responses.create(
        model="gpt-4o-mini",
        tools=[{"type": "web_search_preview"}],
        input=f"List the urls of the mcp servers that are related to {query}"
    )
    return response.output_text

print(list_mcp_from_web_search("video editing"))