from browser_use import Agent
import asyncio
from dotenv import load_dotenv
from llm_adapter import OpenAIAdapter
import os

load_dotenv()

# Set environment variables for browser-use
os.environ["BROWSER_USE_TIMEOUT"] = "30"
os.environ["BROWSER_USE_BROWSER"] = "chrome"

async def main():
    agent = Agent(
        task="Get me a list of Top MLOps learning resources and summarize the content with citation of the source. Ignore the sources which require a login.",
        llm=OpenAIAdapter(model="gpt-3.5-turbo")
    )

    await agent.run()

asyncio.run(main())