from openai import OpenAI

class LlamaClient:
    def __init__(self, base_url):
        self.client = OpenAI(
                base_url = base_url,
                api_key = "sk-no-key-required"
            )


    def query(self, sys_prompt, user_prompt, temprature=0.5, max_tokens=1024):
        completion = self.client.chat.completions.create(
            model="gemma3:latest",
            # model="llama3",
            # model="phi3:latest",
            # model="qwen:4b",
            temperature=temprature,
            max_tokens=max_tokens,
            messages = [
                {"role": "system",
                 "content": sys_prompt},
                {"role": "user", 
                 "content": user_prompt}
            ],

            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "places_schema",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "rules": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "place_name": {"type": "string"},
                                        "place_addr": {"type": "string"},
                                        "telephone": {"type": "string"}
                                    },
                                    "required": ["place_name", "place_addr"],
                                    "additionalProperties": False
                                }
                            }
                        },
                        "required": ["rules"],
                        "additionalProperties": False
                    }
                }
            },
        )
        return completion

# 使用示例
if __name__ == "__main__":

    client = LlamaClient(
        # base_url="http://localhost:6060/v1",        
        base_url="http://localhost:11434/v1",        
    )

    sys_prompt = "You are an AI assistant! You always generate json output for the user's prompt"
    
    user_prompt = "Top 3 most famous places in Beijing, result in JSON."

    code_result = client.query(sys_prompt=sys_prompt, user_prompt=user_prompt, temprature=2)

    # print(code_result.choices[0]["message"]["content"])
    print(code_result.choices[0].message.content)
    # print(code_result["choices"][0]["message"]["content"])