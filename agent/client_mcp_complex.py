# Use langchain to combine playwright

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_deepseek import ChatDeepSeek 
from langchain_ollama import ChatOllama

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
import asyncio

server_params = StdioServerParameters(
    command="npx", 
    args=["@playwright/mcp@latest"]
)

llm = ChatDeepSeek(model="deepseek-chat") # 在命令行设置对应的API-Key
llm_ollama = ChatOllama(model="qwen3:latest",    
                        base_url="http://127.0.0.1:11434",
                        temperature=0.7               
                        )

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
            # agent = create_react_agent(model=llm_ollama, tools=tools)
            agent_response = await agent.ainvoke({"messages": "please navigate to https://www.baidu.com"})
            
            print("💬 Agent Response:", agent_response['messages'])
            print("✅ Tool Response:", agent_response['messages'][2].content);


if __name__ == "__main__":
    asyncio.run(run_server())
