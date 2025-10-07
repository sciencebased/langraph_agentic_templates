#REACT AGENT
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
load_dotenv()

from src.agents.support.nodes.booking.tools import tools
from src.agents.support.nodes.booking.prompt import SYSTEM_PROMPT

agent = create_react_agent(
    model="openai:gpt-4o-mini",
    tools=tools,
    prompt=SYSTEM_PROMPT
)