from langgraph.prebuilt import create_react_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_react_agent(
    model="openai:gpt-4o-mini", # Model of reasoning
    tools=[get_weather],
    prompt="You are a helpful assistant"
)