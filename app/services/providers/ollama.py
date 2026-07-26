import requests


class OllamaProvider:

    def __init__(self, url: str):
        self.url = url.rstrip("/")

    def generate(self, prompt: str) -> str:

        response = requests.post(
            f"{self.url}/api/generate",
            json={
                "model": "llama3.1",
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()

        return response.json()["response"]