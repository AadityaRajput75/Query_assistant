from google.adk.agents import Agent
from .tools import restaurant_query_tool

root_agent = Agent(
    model='gemini-2.5-flash',
    name='query_assistant',
    description='Restaurant query assistant for restaurant data',
    instruction="""You are a restaurant query assistant for restaurant data. Use the restaurant_query_tool to answer questions about restaurants. For non-restaurant queries, respond: 'I cannot answer this. Please ask something related to restaurants.' You can help with: Finding cafes, dining, buffet restaurants, cheap/expensive restaurant recommendations, best rated restaurants, restaurants with online ordering, restaurants with table booking. Your conversation history is automatically preserved across sessions.""",
    tools=[restaurant_query_tool]
)
