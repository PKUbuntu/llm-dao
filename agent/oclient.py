from ollama import Client

OLLAMA_HOST="http://localhost:6060"

client = Client(host=OLLAMA_HOST)

response = client.chat(model='qwen:4b', messages=[
    {
        'role': 'user',
        'content': '你会干什么？',
    },
])


print(response['message']['content'])


stream = client.chat(
    model='qwen:4b', 
    messages=[
        {
            'role': 'user',
            'content': 'write a python code to generate database schema in sql from a excel file',
        },
        ],
    stream=True
)


for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)
