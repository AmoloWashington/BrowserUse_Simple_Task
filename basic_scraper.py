"""
Actually working browser automation with proper LLM setup
"""
import asyncio
import json
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["ANONYMIZED_TELEMETRY"] = "false"

class SimpleLLM:
    def __init__(self, api_key=None):
        from openai import AsyncOpenAI
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
        self.model_name = "gpt-4o-mini"  # ADD THIS LINE
        self.provider = "openai"
    
    async def ainvoke(self, messages):
        """Handle LLM calls"""
        try:
            if hasattr(messages, 'content'):
                content = messages.content
            elif isinstance(messages, list) and len(messages) > 0:
                content = str(messages[-1])
            else:
                content = str(messages)
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": content}],
                temperature=0.7
            )
            
            class Response:
                def __init__(self, content):
                    self.content = content
            
            return Response(response.choices[0].message.content)
            
        except Exception as e:
            print(f"LLM Error: {e}")
            raise

async def working_hacker_news_scraper():
    """Actually working Hacker News scraper"""
    try:
        from browser_use import Agent
        llm = SimpleLLM(api_key=os.getenv("OPENAI_API_KEY"))
        
        agent = Agent(
            task="""
            Go to https://news.ycombinator.com/show
            Wait for the page to load completely.
            Find the first 5 'Show HN' posts.
            
            For each post, extract:
            1. The title (main headline)
            2. The URL/link
            3. Number of comments (look for "X comments")
            4. Hours since posted (look for "X hours ago")
            
            Present this information clearly like:
            
            Post 1:
            Title: [title here]
            URL: [url here]
            Comments: [number]
            Hours ago: [number]
            
            Post 2:
            [etc...]
            """,
            llm=llm
        )
        
        print("🚀 Starting Hacker News scraping...")
        history = await agent.run()
        
        result = history.final_result()
        if result:
            print("✅ Hacker News scraping completed!")
            print("\n" + "="*50)
            print("HACKER NEWS RESULTS:")
            print("="*50)
            print(result)
            return result
        else:
            print("❌ No results from Hacker News")
            return None
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

async def working_google_search():
    """Actually working Google search"""
    try:
        from browser_use import Agent
        
        # Create LLM
        llm = SimpleLLM(api_key=os.getenv("OPENAI_API_KEY"))
        
        agent = Agent(
            task="""
            Go to Google.com
            Search for "MLOps tutorial free beginner"
            Look at the first 5 search results.
            
            For each result, tell me:
            1. The title
            2. The URL
            3. A brief description from the snippet
            
            Present like:
            
            Result 1:
            Title: [title]
            URL: [url]
            Description: [description]
            
            Result 2:
            [etc...]
            """,
            llm=llm
        )
        
        print("🔍 Starting Google search...")
        history = await agent.run()
        
        result = history.final_result()
        if result:
            print("✅ Google search completed!")
            print("\n" + "="*50)
            print("GOOGLE SEARCH RESULTS:")
            print("="*50)
            print(result)
            return result
        else:
            print("❌ No results from Google search")
            return None
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

async def simple_test():
    """Super simple test"""
    try:
        from browser_use import Agent
        
        llm = SimpleLLM(api_key=os.getenv("OPENAI_API_KEY"))
        
        agent = Agent(
            task="Go to https://example.com and tell me what you see",
            llm=llm
        )
        
        print("🧪 Running simple test...")
        history = await agent.run()
        
        result = history.final_result()
        if result:
            print("✅ Simple test PASSED!")
            print(f"Result: {result}")
            return True
        else:
            print(" Simple test failed - no result")
            return False
        
    except Exception as e:
        print(f" Simple test error: {e}")
        return False

async def main():
    """Main function"""
    print(" ACTUALLY WORKING BROWSER AUTOMATION")
    print("=" * 60)
    
    # Test 1: Simple functionality test
    print("\n Test 1: Basic Functionality")
    print("-" * 40)
    basic_works = await simple_test()
    
    if not basic_works:
        print(" Basic test failed. Check your setup.")
        return
    
    # Small delay
    await asyncio.sleep(3)
    
    # Test 2: Hacker News
    print("\n Test 2: Hacker News Scraping")
    print("-" * 40)
    hn_result = await working_hacker_news_scraper()
    
    # Small delay
    await asyncio.sleep(5)
    
    # Test 3: Google Search
    print("\n Test 3: Google MLOps Search")
    print("-" * 40)
    google_result = await working_google_search()
    
    # Save results
    results = {
        "timestamp": str(asyncio.get_event_loop().time()),
        "hacker_news": hn_result,
        "google_search": google_result
    }
    
    with open("working_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "=" * 60)
    print(" ALL TESTS COMPLETED!")
    print(" Results saved to working_results.json")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
