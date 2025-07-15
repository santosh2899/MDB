from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from db_layer import fetch_fields, fetch_logs, fetch_data
from chatbot import generate_chatbot_response

app = FastAPI()

class ChatbotInput(BaseModel):
    workflow_id: int
    question: str

class FieldQuery(BaseModel):
    workflow_id: int
    fields: Optional[List[str]] = None
    filter: Optional[dict] = {}

@app.get("/fields")
def get_fields(workflow_id: int):
    return {
        "workflow_id": workflow_id,
        "fields": fetch_fields(workflow_id)
    }

@app.post("/chatbot")
def chatbot_query(input: ChatbotInput):
    logs = fetch_logs(input.workflow_id)
    response = generate_chatbot_response(logs, input.question)
    return {"answer": response}

@app.post("/data")
def get_filtered_data(query: FieldQuery):
    data = fetch_data(query.workflow_id, query.filter)
    if query.fields:
        return [{k: item.get(k) for k in query.fields} for item in data]
    return data
