from typing import Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import json

class OpenAIAdapter:
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.llm = ChatOpenAI(model=model)
        self.model_name = model  # Add this required attribute
        self.provider = "openai"
        self.model = model  # Some versions might look for this instead
    
    async def ainvoke(self, input: Any, config: Optional[dict] = None, **kwargs) -> Any:
        try:
            # Convert all input types to messages
            if isinstance(input, str):
                messages = [HumanMessage(content=input)]
            elif isinstance(input, dict):
                if 'items' in input:  # Handle browser-use's items format
                    content = json.dumps(input['items'])
                else:
                    content = json.dumps(input)
                messages = [HumanMessage(content=content)]
            else:
                messages = [HumanMessage(content=str(input))]
            
            return await self.llm.ainvoke(messages, config=config, **kwargs)
        except Exception as e:
            print(f"Error processing input: {e}")
            raise ValueError(f"Failed to process input: {str(e)}")
    
    # Add this to delegate any missing attributes to the underlying LLM
    def __getattr__(self, name):
        return getattr(self.llm, name)