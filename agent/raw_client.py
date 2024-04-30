from llama_cpp import Llama
from .response_format import sample_list_format

model_file = "/Users/liuyuan/workspace/llama/model/qwen1_5-1_8b-chat-q8_0.gguf"


class LlamaClient:
    def __init__(self, url):
        self.url = url

    def send_prompt(self, prompt):
        self.prompt = prompt
        pass    



llm = Llama(model_path=model_file, 
        n_gpu_layers=-1, 
        chat_format="chatml")

output = llm.create_chat_completion(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that outputs in JSON.",
        },
        {"role": "user", "content": "Top 3 famous places in Beijing"},
    ],
    response_format={
        "type": "json_object",
        "schema": {
            "type": "object",
            "$defs": { 
                "A": {
                    "type": "object",
                    "properties": {
                        "place_name": {"type": "string", "description": "eg: 长城(Great Wall)"},
                        "place_addr": {"type": "string", "description": "Address of the place"},
                        "telephone": {"type": "string", "description": "telephone number, only need 1"}
                    },
                    "required": ["place_name", "place_addr"],
                }
            },

            "properties": {
                "rules": {
                    "items": {
                        "$ref": "#/$defs/A"
                    },
                    "type": "array"
                }
            },
            "required": ["rules"]
        }
    },
    temperature=0.7,
)


print(output["choices"][0]["message"]["content"])
