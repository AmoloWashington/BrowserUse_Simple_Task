"""
MLOps search with fixed LangChain integration
"""
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

load_dotenv()

os.environ["BROWSER_USE_TIMEOUT"] = "120"
os.environ["BROWSER_USE_BROWSER"] = "chrome"
os.environ["BROWSER_USE_DEBUG"] = "true"
os.environ["ANONYMIZED_TELEMETRY"] = "false"
os.environ["BROWSER_USE_HEADFUL"] = "true"

class FixedChatOpenAI(ChatOpenAI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ainvoke = "openai"
        
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)

async def main():
    try:
        llm = FixedChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        task = """
        Go to Google and search for "MLOps learning resources free".
        Look at the first 10 search results.
        For each result that appears to be a free learning resource (not requiring payment or login), provide:
        
        1. Title of the resource
        2. URL
        3. Brief description of what it offers
        4. Type (course, tutorial, documentation, etc.)
        
        Focus on resources from reputable sources like:
        - Google Cloud, AWS, Azure documentation
        - University courses (Stanford, MIT, etc.)
        - Open source project documentation
        - Well-known tech blogs
        
        Present the information in a clear, organized format.
        """
        
        agent = Agent(task=task, llm=llm)
        
        print("Starting MLOps resource search...")
        await agent.run()
        print("\n✓ MLOps search completed")
        
    except Exception as e:
        print(f"Error running agent: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
