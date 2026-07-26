import os

from app.config import GEMINI_API_KEY

from app.services.providers.gemini import GeminiProvider
from app.services.providers.groq import GroqProvider
from app.services.providers.glm import GLMProvider
from app.services.providers.openrouter import OpenRouterProvider
from app.services.providers.ollama import OllamaProvider


providers = []

if GEMINI_API_KEY:
    providers.append(GeminiProvider(GEMINI_API_KEY))

if os.getenv("GROQ_API_KEY"):
    providers.append(GroqProvider(os.getenv("GROQ_API_KEY")))

if os.getenv("GLM_API_KEY"):
    providers.append(GLMProvider(os.getenv("GLM_API_KEY")))

if os.getenv("OPENROUTER_API_KEY"):
    providers.append(OpenRouterProvider(os.getenv("OPENROUTER_API_KEY")))

if os.getenv("OLLAMA_URL"):
    providers.append(OllamaProvider(os.getenv("OLLAMA_URL")))


def ask_llm(prompt: str) -> str:

    last_error = None

    for provider in providers:

        try:
            return provider.generate(prompt)

        except Exception as e:
            print(f"Provider failed: {provider.__class__.__name__}")
            last_error = e

    raise RuntimeError(
        f"All AI providers failed.\nLast error: {last_error}"
    )