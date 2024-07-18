from openai import OpenAI
from pydantic import BaseModel, Field

import instructor

class Scenery(BaseModel):
    name: str = Field(..., description="name of the place")
    location: str = Field(..., description="location of the place")
    phone_number: str = Field(..., description="telephone number of the place")

class SceneryList(BaseModel):
    sceneries: list[Scenery] = Field(..., description="list of sceneries")

class LlamaClient:
    def __init__(self, base_url):
        self.client =  instructor.patch(
            OpenAI(
                base_url = base_url,
                api_key = "sk-no-key-required"
            ),     
            mode=instructor.Mode.JSON,
        )

    def query(self, sys_prompt, user_prompt, temprature=0.5, max_tokens=1024):
        completion = self.client.chat.completions.create(
            model="llama3:latest",
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
            response_model=SceneryList,
            max_retries=10            
        )
        return completion

    def save_code_to_file(self, code, filename="output.json"):
        with open(filename, "w") as file:
            file.write(code)

# 使用示例
if __name__ == "__main__":

    client = LlamaClient(
        base_url="http://localhost:6060/v1",        
    )

    sys_prompt = "You are an AI assistant! You always generate json output for the user's prompt"
    
    user_prompt = "Top 3 most famous places in New York."

    code_result = client.query(sys_prompt=sys_prompt, user_prompt=user_prompt, temprature=2)

    client.save_code_to_file(code_result.model_dump_json(indent=2), "result.json")
