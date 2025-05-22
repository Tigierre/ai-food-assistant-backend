from fastapi import FastAPI, Request
from langchain_openai import ChatOpenAI
import os

app = FastAPI()

# Inizializza il modello LLM (GPT-4o-mini, puoi cambiare model_name se vuoi)
llm = ChatOpenAI(
    openai_api_key=os.environ["OPENAI_API_KEY"],
    model_name="gpt-4o-mini",
    temperature=0.2
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    if not prompt:
        return {"error": "No prompt provided"}
    # Invoca direttamente il modello (stateless, senza memoria)
    response = llm.invoke(prompt)
    return {"response": response.content}
