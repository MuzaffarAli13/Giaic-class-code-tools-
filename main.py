from agents import Agent,Runner,OpenAIChatCompletionsModel,set_tracing_disabled
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

agent = Agent(
    name="Helper",
    instructions="You are a helpful assistant that can answer questions and help with tasks.",
    model=model
)

async def main():
  result = Runner.run_streamed(
      starting_agent=agent,
      input="What is the capital of France?",
  )
  async for event in result.stream_events():
      if event.type == "raw_response_event" and isinstance(event.data,ResponseTextDeltaEvent):
          print(event.data.delta,end="",flush=True)

if __name__ == "__main__":
    asyncio.run(main())


