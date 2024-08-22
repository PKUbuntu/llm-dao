import ollama
client = ollama.Client()

# 获取当前的所有 Models
models = ollama.list()

model_options = []
for m in models['models']:
    model_options.append(m['model'])

    