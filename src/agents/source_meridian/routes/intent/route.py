from pydantic import BaseModel, Field
from typing import Literal
from langchain.chat_models import init_chat_model
from agents.support.state import State
from agents.support.routes.intent.prompt import SYSTEM_PROMPT

class RouteIntent(BaseModel):
    step: Literal["conversation", "relevant_questions"] = Field(
        'conversation', description="The next step in the routing process"
    )

llm = init_chat_model("openai:gpt-4o", temperature=0)
llm = llm.with_structured_output(schema=RouteIntent)

def intent_route(state: State) -> Literal["conversation", "relevant_questions"]:
    history = state["messages"]
    print('*'*100)
    print(history)
    print('*'*100)
    schema = llm.invoke([("system", SYSTEM_PROMPT)] + history)
    if schema.step is not None:
        return schema.step
    return 'conversation'