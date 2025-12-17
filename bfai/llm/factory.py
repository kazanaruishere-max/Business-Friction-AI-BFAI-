from bfai.llm.llm_interface import LLMProvider
from bfai.llm.mock_provider import MockLLMProvider

def get_llm_provider(mode: str = "mock") -> LLMProvider:
    """
    Factory to get the appropriate LLM provider.
    
    Args:
        mode: 'mock' (default) or 'gemini' (future).
    """
    if mode == "mock":
        return MockLLMProvider()
    
    # Future:
    # if mode == "gemini":
    #     return GeminiLLMProvider()
        
    raise ValueError(f"Unknown LLM provider mode: {mode}")
