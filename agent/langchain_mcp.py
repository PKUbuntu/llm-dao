# 
# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_deepseek import ChatDeepSeek 
from langchain_ollama import ChatOllama

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
import asyncio

server_params = StdioServerParameters(
    command="uv", 
    # args=["run", "mcp", "dev", "./mcp/echo.py"]
    args=["run", "mcp", "run", "./tools/echo.py"]    
)

# You can choose other models like "deepseek-coder" if needed

llm = ChatDeepSeek(model="deepseek-chat") # 在命令行设置对应的API-Key
llm_ollama = ChatOllama(model="qwen3:latest")

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
            agent_response = await agent.ainvoke({"messages": "please echo with me: Hola!"})
            
            print("💬 Agent Response:", agent_response['messages'])
            print("✅ Tool Response:", agent_response['messages'][2].content);


if __name__ == "__main__":
    asyncio.run(run_server())

""" The response of the above:
[
  HumanMessage(content='please echo with me: Hola!', additional_kwargs={}, response_metadata={}, id='794bd935-391b-4ef8-99f5-257149c6d4f0'), 
  AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_0_2cb12371-73bd-40b1-94e6-17264f15d4e6', 'function': {'arguments': '{"text":"Hola!"}', 'name': 'echo'}, 'type': 'function', 'index': 0}], 'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 19, 'prompt_tokens': 115, 'total_tokens': 134, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 64}, 'prompt_cache_hit_tokens': 64, 'prompt_cache_miss_tokens': 51}, 'model_name': 'deepseek-chat', 'system_fingerprint': 'fp_8802369eaa_prod0623_fp8_kvcache', 'id': 'b2fb963a-61b4-4bef-8a89-cfa7d7a709f2', 'service_tier': None, 'finish_reason': 'tool_calls', 'logprobs': None}, id='run--953d8901-6d7e-4314-9d6c-ac2af54c1247-0', tool_calls=[{'name': 'echo', 'args': {'text': 'Hola!'}, 'id': 'call_0_2cb12371-73bd-40b1-94e6-17264f15d4e6', 'type': 'tool_call'}], usage_metadata={'input_tokens': 115, 'output_tokens': 19, 'total_tokens': 134, 'input_token_details': {'cache_read': 64}, 'output_token_details': {}}),
  ToolMessage(content='You said: Hola!', name='echo', id='92136b0a-c995-4aa7-bad6-bb35a614c7ee', tool_call_id='call_0_2cb12371-73bd-40b1-94e6-17264f15d4e6'),
  AIMessage(content='Got it! You said: Hola! 😊', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 11, 'prompt_tokens': 146, 'total_tokens': 157, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 128}, 'prompt_cache_hit_tokens': 128, 'prompt_cache_miss_tokens': 18}, 'model_name': 'deepseek-chat', 'system_fingerprint': 'fp_8802369eaa_prod0623_fp8_kvcache', 'id': '91e28d38-c65c-46b7-9ae3-e49fc8cef6ac', 'service_tier': None, 'finish_reason': 'stop', 'logprobs': None}, id='run--d8a28217-0a76-4ffc-a6f5-f5139c3c0fb6-0', usage_metadata={'input_tokens': 146, 'output_tokens': 11, 'total_tokens': 157, 'input_token_details': {'cache_read': 128}, 'output_token_details': {}})
]
"""
