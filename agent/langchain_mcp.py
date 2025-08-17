# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_deepseek import ChatDeepSeek 

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
import asyncio

server_params = StdioServerParameters(
    command="uv", 
    # args=["run", "mcp", "dev", "./mcp/echo.py"]
    args=["run", "mcp", "run", "./tools/echo.py"]    
)

# You can choose other models like "deepseek-coder" if needed
llm = ChatDeepSeek(model="deepseek-chat")

async def run_server():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)
            print("🔧 Available tools:", tools)

            # Create and run the agent
            agent = create_react_agent(model=llm, tools=tools)
            agent_response = await agent.ainvoke({"messages": "please echo with me: Hola!"})
            
            print("💬 Agent Response:", agent_response["message"])


if __name__ == "__main__":
    asyncio.run(run_server())
