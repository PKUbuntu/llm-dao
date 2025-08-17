import requests
from langchain_ollama import ChatOllama

# 显式指定 Ollama 服务地址（Windows 建议用 127.0.0.1，而不是 localhost/::1）
OLLAMA_HOST = "http://127.0.0.1:11434"

def check_ollama_server():
    """检查 Ollama 服务是否运行"""
    try:
        resp = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if resp.status_code == 200:
            print("✅ Ollama 服务已连接成功")
            print("可用模型列表:", [m["name"] for m in resp.json().get("models", [])])
            return True
        else:
            print("⚠️ Ollama 服务返回异常:", resp.status_code)
    except Exception as e:
        print("❌ 无法连接 Ollama 服务:", e)
    return False


def main():
    if not check_ollama_server():
        print("请确认 Ollama 已启动，并执行过: ollama pull qwen3")
        return

    # 初始化 LangChain Ollama
    llm = ChatOllama(
        model="qwen3:latest",                # 确保你已拉取: ollama pull llama3
        base_url=OLLAMA_HOST,          # 显式指定服务地址
        temperature=0.7
    )

    # 测试调用
    response = llm.invoke("用三句话介绍一下量子计算。")
    print("\n🤖 模型输出:\n", response.content)


if __name__ == "__main__":
    main()
