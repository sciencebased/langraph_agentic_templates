#REACT AGENT
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
load_dotenv()

from src.agents.support.nodes.relevant_questions.tools import tools
from src.agents.support.nodes.relevant_questions.prompt import SYSTEM_PROMPT
from agents.support.state import State

agent = create_react_agent(
    model="openai:gpt-4o-mini",
    tools=tools,
    prompt=(SYSTEM_PROMPT)
)