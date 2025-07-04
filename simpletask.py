from browser_use import Agent
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

# Set environment variables for browser-use
os.environ["BROWSER_USE_TIMEOUT"] = "90"
os.environ["BROWSER_USE_BROWSER"] = "chrome"
os.environ["BROWSER_USE_DEBUG"] = "true"
os.environ["ANONYMIZED_TELEMETRY"] = "false"

class FlexibleChatOpenAI:
    """A flexible wrapper that allows browser-use to inject methods"""
    def __init__(self):
        from openai import AsyncOpenAI
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"
        self.model_name = "gpt-4o-mini"
        self.provider = "openai"
    
        for attr in dir(self._llm):
            if not attr.startswith('_'):
                setattr(self, attr, getattr(self._llm, attr))
    
    def __getattr__(self, name):
        
        return getattr(self._llm, name)
    
    def __setattr__(self, name, value):
        super().__setattr__(name, value)

async def main():
    try:
        llm = FlexibleChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        task = """
        Search for 'MLOps learning resources' and 'MLOps best practices' on Google.
        Find the top 10 learning resources that are freely accessible (no login required).
        For each resource, provide:
        1. Title of the resource
        2. URL
        3. Brief summary of what it covers (2-3 sentences)
        4. Type (course, tutorial, documentation, blog post, etc.)
        5. Difficulty level (beginner, intermediate, advanced)
        
        Focus on high-quality, reputable sources like:
        - Official documentation
        - University courses
        - Well-known tech blogs
        - Open source projects
        - Industry publications
        
        Ignore sources that require paid subscriptions or mandatory registration.
        """
        
        agent = Agent(task=task, llm=llm)
        
        print("Starting MLOps resource search...")
        await agent.run()
        print("\n✓ MLOps resource search completed")
        
    except Exception as e:
        print(f"Error running agent: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
