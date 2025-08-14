# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
import asyncio

server_params = StdioServerParameters(
    command="npx",
    # Make sure to update to the full absolute path to your math_server.py file
    args=["@playwright/mcp@latest"],
)

async def run_server():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create and run the agent
            agent = create_react_agent("openai:gpt-4.1", tools)
            agent_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})

def main():
    asyncio.run(run_server())