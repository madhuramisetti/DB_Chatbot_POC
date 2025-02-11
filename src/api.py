from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from config import DB_CONFIG, MODEL_CONFIG
from chatbot import DatabaseChatbot

app = FastAPI()
chatbot = DatabaseChatbot(DB_CONFIG, MODEL_CONFIG)

class Query(BaseModel):
    question: str

@app.post("/query")
async def process_query(query: Query):
    result = chatbot.process_query(query.question)
    if result['status'] == 'error':
        raise HTTPException(status_code=400, detail=result['message'])
    return result