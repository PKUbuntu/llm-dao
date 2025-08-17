
from langchain_ollama import ChatOllama

# 初始化 Ollama 模型
llm = ChatOllama(
    model="qwen3:latest",  # 模型名，比如 llama3、qwen2、mistral
    base_url="http://127.0.0.1:11434",
    temperature=0.7
)

# 简单对话
response = llm.invoke("用三句话介绍一下量子计算。")
print(response.content)
