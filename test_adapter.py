#!/usr/bin/env python3
"""
Simple test for the LLM adapter
"""

import asyncio
from llm_adapter import OpenAIAdapter
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

async def test_adapter():
    print("Testing LLM Adapter...")
    
    adapter = OpenAIAdapter(model="gpt-3.5-turbo")
    
    # Test with different input types
    test_cases = [
        # String input
        "Hello, this is a test",
        
        # List of LangChain messages (similar to what BrowserUse sends)
        [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content="Say hello")
        ],
        
        # Dictionary input
        {"test": "message", "type": "dict"}
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        try:
            print(f"\nTest {i}: {type(test_input).__name__}")
            print(f"Input: {str(test_input)[:100]}...")
            
            result = await adapter.ainvoke(test_input)
            print(f"✓ Success: {result.content[:50]}...")
            
        except Exception as e:
            print(f"✗ Failed: {e}")
    
    print("\nLLM Adapter test completed!")

if __name__ == "__main__":
    asyncio.run(test_adapter())
