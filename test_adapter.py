"""
Minimal test to verify everything works
"""
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

class MinimalLLM:
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
            messages=[{"role": "user", "content": content}]
        )
        
        class Resp:
            def __init__(self, content):
                self.content = content
        
        return Resp(response.choices[0].message.content)

async def main():
    try:
        from browser_use import Agent
        
        print("🧪 Testing minimal setup...")
        
        llm = MinimalLLM()
        agent = Agent(
            task="Go to https://httpbin.org/json and describe the JSON you see",
            llm=llm
        )
        
        result = await agent.run()
        
        if result and result.final_result():
            print("✅ SUCCESS! Browser automation is working!")
            print(f"Result: {result.final_result()}")
        else:
            print("❌ Failed - no result")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
