# NOTE: Use default(OpenAI) to connect Ollama
# Or can use langchain_ollama to connect Ollama

from langchain.chat_models import init_chat_model

llm = init_chat_model("qwen3:latest",
                      model_provider="ollama", base_url="http://127.0.0.1:11434")

# use streaming mode
for trunk in llm.stream("Hi!"):
    print(trunk.text(), end="")

# compact mode
llm_2 = init_chat_model("ollama:qwen3", base_url="http://127.0.0.1:11434")

for trunk in llm_2.stream("你好!"):
    print(trunk.text(), end="")

# Also can use DeepSeek provider

