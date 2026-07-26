import requests


class OpenRouterProvider:

    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate(self, prompt: str) -> str:

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "meta-llama/llama-3.3-70b-instruct",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            },
            timeout=120,
        )

        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]