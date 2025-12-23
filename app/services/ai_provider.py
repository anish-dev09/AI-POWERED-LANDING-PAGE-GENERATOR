"""
AI Provider Factory - Handles switching between Gemini and OpenAI.
"""
import os
from abc import ABC, abstractmethod
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    @abstractmethod
    async def generate_content(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate content using the AI provider."""
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Get the name of the provider."""
        pass


class GeminiProvider(AIProvider):
    """Google Gemini AI provider."""
    
    def __init__(self):
        """Initialize Gemini provider."""
        try:
            import google.generativeai as genai
            self.genai = genai
            
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables")
            
            self.genai.configure(api_key=api_key)
            
            model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
            self.model = self.genai.GenerativeModel(model_name)
            
        except ImportError:
            raise ImportError("google-generativeai package not installed. Install with: pip install google-generativeai")
    
    async def generate_content(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        Generate content using Gemini.
        
        Args:
            prompt: The prompt to send to Gemini
            max_tokens: Maximum tokens to generate (Gemini uses max_output_tokens)
            
        Returns:
            Generated content as string
        """
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.genai.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.7,
                )
            )
            return response.text
        except Exception as e:
            raise Exception(f"Gemini content generation failed: {str(e)}")
    
    def get_provider_name(self) -> str:
        """Get provider name."""
        return "Gemini"


class OpenAIProvider(AIProvider):
    """OpenAI GPT provider."""
    
    def __init__(self):
        """Initialize OpenAI provider."""
        try:
            from openai import AsyncOpenAI
            
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            
            self.client = AsyncOpenAI(api_key=api_key)
            self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            
        except ImportError:
            raise ImportError("openai package not installed. Install with: pip install openai")
    
    async def generate_content(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        Generate content using OpenAI.
        
        Args:
            prompt: The prompt to send to OpenAI
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated content as string
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert marketing copywriter specializing in landing pages."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI content generation failed: {str(e)}")
    
    def get_provider_name(self) -> str:
        """Get provider name."""
        return "OpenAI"


class AIProviderFactory:
    """Factory to create and manage AI providers."""
    
    _instance: Optional[AIProvider] = None
    
    @classmethod
    def get_provider(cls, provider_name: Optional[str] = None) -> AIProvider:
        """
        Get AI provider instance (singleton pattern).
        
        Args:
            provider_name: Name of provider ('gemini' or 'openai'). 
                          If None, uses AI_PROVIDER from environment.
        
        Returns:
            AIProvider instance
        
        Raises:
            ValueError: If provider name is invalid or not configured
        """
        if cls._instance is not None:
            return cls._instance
        
        if provider_name is None:
            provider_name = os.getenv("AI_PROVIDER", "gemini").lower()
        
        try:
            if provider_name == "gemini":
                cls._instance = GeminiProvider()
            elif provider_name == "openai":
                cls._instance = OpenAIProvider()
            else:
                raise ValueError(f"Unknown AI provider: {provider_name}. Use 'gemini' or 'openai'")
            
            print(f"✓ AI Provider initialized: {cls._instance.get_provider_name()}")
            return cls._instance
            
        except Exception as e:
            # Try fallback provider
            if provider_name == "gemini":
                print(f"⚠ Gemini failed ({str(e)}), trying OpenAI fallback...")
                try:
                    cls._instance = OpenAIProvider()
                    print(f"✓ Fallback AI Provider initialized: OpenAI")
                    return cls._instance
                except Exception as fallback_error:
                    raise Exception(f"Both providers failed. Gemini: {str(e)}, OpenAI: {str(fallback_error)}")
            else:
                raise Exception(f"Failed to initialize {provider_name}: {str(e)}")
    
    @classmethod
    def reset(cls):
        """Reset the provider instance (useful for testing)."""
        cls._instance = None


# Convenience function
async def generate_ai_content(prompt: str, max_tokens: int = 1000) -> str:
    """
    Generate content using the configured AI provider.
    
    Args:
        prompt: The prompt to send to AI
        max_tokens: Maximum tokens to generate
        
    Returns:
        Generated content as string
    """
    provider = AIProviderFactory.get_provider()
    return await provider.generate_content(prompt, max_tokens)
