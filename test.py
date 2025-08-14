import ollama

OLLAMA_HOST="http://localhost:11434"

client = ollama.Client(host=OLLAMA_HOST)

response = client.chat(
    # model='gemma3:12b',
    model = 'llama3.2-vision:latest',
    messages=[{
        'role': 'user',
        'content': ' 请描述一下图中的内容',
        'images': ['F:\\OneDrive\\Pictures\\sig3.jpg']
    }]
)

print(response)


