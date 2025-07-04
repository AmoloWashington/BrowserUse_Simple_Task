from typing import Any, Optional, Union, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
import json

class OpenAIAdapter:
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.llm = ChatOpenAI(model=model)
        self.model_name = model
        self.provider = "openai"
        self.model = model

    async def ainvoke(self, input: Any, config: Optional[dict] = None, **kwargs) -> Any:
        try:
            # Handle different input types for BrowserUse compatibility
            messages = self._convert_to_messages(input)
            return await self.llm.ainvoke(messages, config=config, **kwargs)
        except Exception as e:
            print(f"Error in OpenAIAdapter.ainvoke: {e}")
            print(f"Input type: {type(input)}")
            # Create a fallback message for debugging
            fallback_messages = [HumanMessage(content=f"Error processing input: {str(e)[:200]}...")]
            return await self.llm.ainvoke(fallback_messages, config=config, **kwargs)

    def _convert_to_messages(self, input: Any) -> List[BaseMessage]:
        """Convert various input types to LangChain messages"""
        try:
            if isinstance(input, str):
                return [HumanMessage(content=input)]

            elif isinstance(input, list):
                # Check if it's already a list of LangChain message objects
                if input and isinstance(input[0], BaseMessage):
                    # Already LangChain messages, return as-is
                    return input
                elif input and hasattr(input[0], 'content'):
                    # It's a list of message-like objects, return as-is
                    return input
                else:
                    # Convert non-message list to string representation
                    try:
                        content = str(input)  # Use str() instead of json.dumps for complex objects
                    except:
                        content = f"List with {len(input)} items"
                    return [HumanMessage(content=content)]

            elif isinstance(input, dict):
                # Handle dictionary input
                try:
                    content = json.dumps(input, ensure_ascii=False, indent=2)
                except:
                    content = str(input)
                return [HumanMessage(content=content)]

            elif isinstance(input, BaseMessage):
                # Single message object
                return [input]

            elif hasattr(input, 'content'):
                # Single message-like object
                return [input]

            else:
                # Fallback: convert to string
                return [HumanMessage(content=str(input))]

        except Exception as e:
            print(f"Error in _convert_to_messages: {e}")
            # Ultimate fallback
            return [HumanMessage(content=f"Conversion error occurred")]

    def invoke(self, input: Any, config: Optional[dict] = None, **kwargs) -> Any:
        """Synchronous version for compatibility"""
        messages = self._convert_to_messages(input)
        return self.llm.invoke(messages, config=config, **kwargs)

    # Delegate any missing attributes to the underlying LLM
    def __getattr__(self, name):
        return getattr(self.llm, name)
