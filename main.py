from fastapi import FastAPI, Request
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
import os

app = FastAPI()
llm = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"], model_name="gpt-4o", temperature=0.2)
chain = ConversationChain(llm=llm)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    if not prompt:
        return {"error": "No prompt provided"}
    response = chain.run(prompt)
    return {"response": response}
