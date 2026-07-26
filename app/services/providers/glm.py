import requests


class GLMProvider:

    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate(self, prompt: str) -> str:

        response = requests.post(
            "https://open.bigmodel.cn/api/paas/v4/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "glm-4-flash",
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