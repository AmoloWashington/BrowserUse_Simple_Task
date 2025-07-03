from typing import Any, Optional, Union, List
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage
import json

class LLMWrapper:
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
        self.provider = self._get_provider_name(llm)
        self.model = getattr(llm, "model_name", getattr(llm, "model", "unknown"))
    
    def _get_provider_name(self, llm) -> str:
        """Extract provider name from the LLM class name"""
        class_name = llm.__class__.__name__.lower()
        if 'openai' in class_name:
            return 'openai'
        elif 'google' in class_name or 'gemini' in class_name:
            return 'google'
        elif 'anthropic' in class_name:
            return 'anthropic'
        else:
            return 'unknown'
    
    async def ainvoke(self, input: Any, config: Optional[dict] = None, **kwargs) -> Any:
        """Handle all input types from browser-use"""
        try:
            # Convert all inputs to appropriate format
            if isinstance(input, str):
                messages = [HumanMessage(content=input)]
            elif isinstance(input, list) and all(isinstance(msg, BaseMessage) for msg in input):
                messages = input
            elif isinstance(input, dict):
                if 'page_content' in input:  # Browser-use page object
                    messages = [HumanMessage(content=input['page_content'])]
                else:
                    messages = [HumanMessage(content=json.dumps(input))]
            else:
                messages = [HumanMessage(content=str(input))]
            
            return await self.llm.ainvoke(messages, config=config, **kwargs)
        except Exception as e:
            print(f"Error processing input: {e}")
            raise ValueError(f"Failed to process input: {str(e)}")

    def __getattr__(self, name):
        """Delegate other attribute access to the wrapped LLM"""
        return getattr(self.llm, name)