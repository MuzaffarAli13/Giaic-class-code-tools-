from agents import Agent,Runner,OpenAIChatCompletionsModel,set_tracing_disabled,function_tool,WebSearchTool
from dotenv import load_dotenv
import os
import chainlit as cl
from openai.types.responses import ResponseTextDeltaEvent
from openai import AsyncOpenAI
import asyncio


load_dotenv()
set_tracing_disabled(True)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash"

external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=external_client
)

@function_tool
def get_user_data(user_age:str) -> str:
    "Retrieve user data based on a minimum age"
    users = [
        {"name": "Muneeb", "age": 22},
        {"name": "Muhammad Ubaid Hussain", "age": 25},
        {"name": "Azan", "age": 19},
    ]
    for user in users:
        if user["age"] < int(user_age):
            users.remove(user)
    return users


rishty_wali_agent = Agent(
    name="Rishty Wali",
    instructions="You are a warm and wise 'Rishtey Wali Auntie' who helps people find matches",
    model=model,
    tools=[get_user_data,WebSearchTool()]
)

result = Runner.run_sync(
    starting_agent=rishty_wali_agent,
    input="find a match of 25 minimum age and tell me the details about the match from linkedin",
)

print(result.final_output)

