# client.py
## Run the snippet "uv run agent/client_mcp.py"

import asyncio
from mcp.client.session import ClientSession
from mcp.shared.message import SessionMessage
from mcp.types import JSONRPCMessage, JSONRPCRequest
from mcp.client.stdio import stdio_client, StdioServerParameters

# Import the OpenAI client instead of ollama
from openai import OpenAI
import os
import json

# To use the OpenAI client with a local server like Ollama, 
# you typically point it to the server's OpenAI-compatible endpoint (often ending in /v1).
# The API key can often be a placeholder string like "ollama" for local servers.

client = OpenAI(
    base_url=os.getenv('OPENAI_API_BASE', 'http://localhost:11434/v1'),
    api_key=os.getenv('OPENAI_API_KEY', 'ollama'), # Default key for local Ollama server
)


def build_tools(tools):
    openai_tools = []
    if tools.tools:
        for tool in tools.tools:
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                }
            })
    return openai_tools


async def main():
    # Start MCP server in-process for demo purposes
    async with stdio_client(StdioServerParameters(
            command="uv", 
            # args=["run", "mcp", "dev", "./mcp/echo.py"]
            args=["run", "mcp", "run", "./mcp/echo.py"]
    )) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("🔧 Available tools:", tools)

            # Convert MCP tools to OpenAI format
            openai_tools = build_tools(tools)

            try:
                chat_completion = client.chat.completions.create(
                    model="qwen3:latest", # Ensure this model is served by your endpoint
                    # model = "deepseek-chat",
                    messages=[
                        {
                            "role": "user",
                            "content": "please echo with me: haha",
                        }
                    ],
                    tools=openai_tools,
                    max_tokens=1024, # It's good practice to set a max token limit
                )
                # The response structure is different from the ollama client.
                response_text = chat_completion.choices[0].message.content
                print("💬 OpenAI client response:", response_text)
                tool_call = chat_completion.choices[0].message.tool_calls
                print("💬 Tool Call:", tool_call)

                # 修复：检查 tool_call 是否为 None
                if tool_call:
                    for call in tool_call:
                        # 修复：正确处理不同类型的tool_call
                        if hasattr(call, 'function'):
                            print("💬 Call:", call.function.name)
                            print("💬 Call:", call.function.arguments)
                            tool_response = await session.call_tool(call.function.name, json.loads(call.function.arguments or "{}"))
                        elif hasattr(call, 'custom'):
                            print("💬 Call:", call.custom.name)
                            print("💬 Call:", call.custom.input)
                            tool_response = await session.call_tool(call.custom.name, json.loads(call.custom.input or "{}"))
                        else:
                            print("💬 Unknown tool call type:", call)
                            continue
                        print("💬 Response:", tool_response.content[0].text)

            except Exception as e:
                print(f"❌ Error calling model via OpenAI client: {e}")


if __name__ == "__main__":
    asyncio.run(main())
