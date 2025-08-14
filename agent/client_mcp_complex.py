# client.py
import asyncio
from mcp.shared.message import SessionMessage
from mcp.types import JSONRPCRequest, JSONRPCMessage
from mcp.client.stdio import stdio_client, StdioServerParameters

# Import the OpenAI client instead of ollama
from openai import OpenAI
import os

# To use the OpenAI client with a local server like Ollama, 
# you typically point it to the server's OpenAI-compatible endpoint (often ending in /v1).
# The API key can often be a placeholder string like "ollama" for local servers.

# client = OpenAI(
#     base_url=os.getenv('OPENAI_API_BASE', 'http://localhost:11434/v1'),
#     api_key=os.getenv('OPENAI_API_KEY', 'ollama'), # Default key for local Ollama server
# )

client = OpenAI(
    base_url=os.getenv('DEEPSEEK_API_BASE', 'https://api.deepseek.com/v1'),
    api_key=os.getenv('DEEPSEEK_API_KEY'), # Your DeepSeek API key
)


async def main():
    # Start MCP server in-process for demo purposes
    # npx @playwright/mcp@latest
    async with stdio_client(StdioServerParameters(
            command="npx", 
            args=["@playwright/mcp@latest"]
    )) as (read, write):
        print("✅ Connected to MCP server")

        # Example: Call the model using the OpenAI client
        # The API uses a 'messages' array instead of a single 'prompt'.
        try:
            print("▶️ Calling model via OpenAI client...")
            chat_completion = client.chat.completions.create(
                # model="qwen3:latest", # Ensure this model is served by your endpoint
                model = "deepseek-chat",
                messages=[
                    {
                        "role": "user",
                        "content": "open url https://www.baidu.com?",
                    }
                ],
                max_tokens=100, # It's good practice to set a max token limit
            )
            # The response structure is different from the ollama client.
            response_text = chat_completion.choices[0].message.content
            print("💬 OpenAI client response:", response_text)
        except Exception as e:
            print(f"❌ Error calling model via OpenAI client: {e}")


        # Construct the correct JSONRPCRequest object to send to the MCP server
        request = JSONRPCRequest(
            jsonrpc="2.0",
            method="tools/call",
            params={
                "name": "browser_navigate",
                "arguments": {"url": "https://www.baidu.com"}
            },
            id="1"
        )
        print("▶️ Ready to send message...")
        
        # Construct the SessionMessage object
        message = JSONRPCMessage(request)
        session_message = SessionMessage(message)
        await write.send(session_message)

        print("▶️ Ready to read message...")
        
        async for message in read:
            # Check if the message is an exception
            if isinstance(message, Exception):
                print(f"Error: {message}")
                continue
                
            # Process SessionMessage
            if hasattr(message, 'message'):
                msg = message.message
                # Use getattr to safely access attributes
                method = getattr(msg, 'method', None)
                msg_id = getattr(msg, 'id', None)
                if method == "tools/call" and msg_id == "1":
                    print("🔧 MCP echo result received, exiting.")
                    break

        print("▶️ Read message done!")


if __name__ == "__main__":
    asyncio.run(main())
