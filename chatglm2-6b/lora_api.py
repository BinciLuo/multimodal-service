from transformers import AutoTokenizer, AutoModel
from fastapi import FastAPI
from peft import get_peft_model, LoraConfig, TaskType, PeftConfig, PeftModel
import torch

app = FastAPI()

# 加载模型和标记器
tokenizer = AutoTokenizer.from_pretrained("/home/user/netdisk/data/chatglm2-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("/home/user/netdisk/data/chatglm2-6b", trust_remote_code=True, device='cuda')
model = PeftModel.from_pretrained(model, "/home/user/netdisk/data/multimodal-service/chatglm2-6b/loras/checkpoint-300")
model = model.eval()

with open("chatGPT_head.txt", mode='r') as f:
    prompt = f.read()

from pydantic import BaseModel
class Chat_Chatglm26b_Params(BaseModel):
    query: str
    history: list


@app.post("/chat/chatglm2-6b")
async def chat(params: Chat_Chatglm26b_Params):
    history = [(prompt, "OK")]+[(round[0],round[1]) for round in params.history]
    response, history = model.chat(tokenizer, params.query, history=history)
    return {"chat": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=27777)
