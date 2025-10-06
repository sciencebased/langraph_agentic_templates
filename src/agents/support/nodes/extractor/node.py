from agents.support.state import State
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from agents.support.nodes.extractor.prompt import SYSTEM_PROMPT

class ContactInfo(BaseModel):
    """Contact information of a person"""
    name: str = Field(..., description="The full name of the person")
    email: str = Field(..., description="The email address of the person")
    phone: str = Field(..., description="The phone number of the person")
    age: int = Field(..., description="The age of the person", ge=0, le=100)

llm = init_chat_model("openai:gpt-4.1-mini", temperature=0.5)
llm_with_structured_output = llm.with_structured_output(schema=ContactInfo)

def extractor(state: State):
    new_state: State = {}
    history = state["messages"]
    customer_name = state.get("customer_name", None)
    if customer_name is None or len(history) >= 5:
        schema = llm_with_structured_output.invoke([SYSTEM_PROMPT] + history)
        new_state["customer_name"] = schema.name
        new_state["phone"] = schema.phone
        new_state["my_age"] = schema.age
    return new_state
