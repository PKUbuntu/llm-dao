# TODO: Ollama client 没有正常工作过，暂时不知道问题在哪儿

import ollama
import os

llama_host = "http://" +  os.getenv('OLLAMA_HOST', 'localhost:11434')

client = ollama.Client(host=llama_host)

# 获取当前的所有 Models
models = ollama.list()

model_options = []
for m in models['models']:
    model_options.append(m['model'])

print(model_options)    
