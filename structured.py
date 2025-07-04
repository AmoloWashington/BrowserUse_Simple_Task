"""
Working structured scraper with JSON output
"""
import asyncio
import json
import re
from dotenv import load_dotenv
import os

load_dotenv()

class WorkingLLM:
    def __init__(self):
        from openai import AsyncOpenAI
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"
        self.model_name = "gpt-4o-mini" 
        self.provider = "openai"
    
    async def ainvoke(self, messages):
        content = str(messages)
        if hasattr(messages, 'content'):
            content = messages.content
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": content}],
            temperature=0.3
        )
        
        class Response:
            def __init__(self, content):
                self.content = content
        
        return Response(response.choices[0].message.content)

async def scrape_hacker_news_structured():
    """Scrape Hacker News with structured JSON output"""
    try:
        from browser_use import Agent
        
        llm = WorkingLLM()
        
        agent = Agent(
            task="""
            Go to https://news.ycombinator.com/show
            
            Find exactly 5 'Show HN' posts.
            
            Extract the following information for each post:
            - title: The main headline text
            - url: The link to the post
            - comments: Number of comments (extract number from "X comments")
            - hours_ago: Hours since posted (extract number from "X hours ago")
            
        
            """,
            llm=llm
        )
        
        print("🔍 Scraping Hacker News with structured output...")
        history = await agent.run()
        
        result = history.final_result()
        
        if result:
            # Try to extract JSON from the result
            json_match = re.search(r'\[.*\]', result, re.DOTALL)
            
            if json_match:
                json_str = json_match.group()
                try:
                    data = json.loads(json_str)
                    print(f"✅ Successfully extracted {len(data)} posts!")
                    return data
                except json.JSONDecodeError as e:
                    print(f"❌ JSON decode error: {e}")
                    print(f"Raw JSON: {json_str}")
                    return None
            else:
                print("❌ No JSON found in response")
                print(f"Raw response: {result}")
                return None
        else:
            print("❌ No result from agent")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

async def search_mlops_structured():
    """Search MLOps resources with structured output"""
    try:
        from browser_use import Agent
        
        llm = WorkingLLM()
        
        agent = Agent(
            task="""
            Go to Google.com
            Search for "MLOps tutorial free course"
            
            Look at the first 5 search results that appear to be learning resources.
            
            Extract:
            - title: Page title
            - url: URL
            - description: Brief description from search snippet
            - type: Type of resource (course, tutorial, documentation, etc.)
            """,
            llm=llm
        )
        
        print("🔍 Searching MLOps resources...")
        history = await agent.run()
        
        result = history.final_result()
        
        if result:
            json_match = re.search(r'\[.*\]', result, re.DOTALL)
            
            if json_match:
                json_str = json_match.group()
                try:
                    data = json.loads(json_str)
                    print(f"✅ Successfully found {len(data)} resources!")
                    return data
                except json.JSONDecodeError as e:
                    print(f"❌ JSON decode error: {e}")
                    return None
            else:
                print("❌ No JSON found in response")
                return None
        else:
            print("❌ No result from agent")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

async def main():
    """Main execution"""
    print("🚀 STRUCTURED DATA SCRAPING")
    print("=" * 50)
    
    # Task 1: Hacker News
    print("\n📰 Scraping Hacker News Show HN Posts")
    print("-" * 40)
    hn_data = await scrape_hacker_news_structured()
    
    if hn_data:
        print("\n📊 HACKER NEWS RESULTS:")
        for i, post in enumerate(hn_data, 1):
            print(f"\n{i}. {post.get('title', 'Unknown')}")
            print(f"   URL: {post.get('url', 'N/A')}")
            print(f"   Comments: {post.get('comments', 0)}")
            print(f"   Hours ago: {post.get('hours_ago', 0)}")
    
    # Small delay
    await asyncio.sleep(5)
    
    # Task 2: MLOps search
    print("\n🔍 Searching MLOps Resources")
    print("-" * 40)
    mlops_data = await search_mlops_structured()
    
    if mlops_data:
        print("\n📚 MLOPS RESOURCES:")
        for i, resource in enumerate(mlops_data, 1):
            print(f"\n{i}. {resource.get('title', 'Unknown')}")
            print(f"   URL: {resource.get('url', 'N/A')}")
            print(f"   Description: {resource.get('description', 'N/A')}")
    
    # Save all results
    final_results = {
        "hacker_news_posts": hn_data or [],
        "mlops_resources": mlops_data or [],
        "total_hn_posts": len(hn_data) if hn_data else 0,
        "total_mlops_resources": len(mlops_data) if mlops_data else 0
    }
    
    with open("structured_results.json", "w") as f:
        json.dump(final_results, f, indent=2)
    
    print(f"\n💾 Results saved to structured_results.json")
    print(f"📊 Total: {final_results['total_hn_posts']} HN posts, {final_results['total_mlops_resources']} MLOps resources")
    
    print("\n" + "=" * 50)
    print("🎉 STRUCTURED SCRAPING COMPLETED!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
