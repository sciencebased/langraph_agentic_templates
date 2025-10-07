from typing import Union
from fastapi import FastAPI
from agents.source_meridian.agent import agent
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

class Message(BaseModel):
    message: str
    customer_name: str

@app.post("/chat/{chat_id}")
def chat(chat_id: str, item: Message):
    human_message = HumanMessage(content=item.message)
    response = agent.invoke({"messages": [human_message]})
    last_message = response["messages"][-1]
    return last_message.content