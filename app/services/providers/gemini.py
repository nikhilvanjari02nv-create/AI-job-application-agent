import time

from google import genai
from google.genai.errors import ClientError


class GeminiProvider:

    def __init__(self, api_key: str):

        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt: str) -> str:

        while True:

            try:

                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )

                return response.text

            except ClientError as e:

                error = str(e)

                if (
                    "429" in error
                    or "RESOURCE_EXHAUSTED" in error
                ):

                    raise RuntimeError("RATE_LIMIT")

                raise

            except Exception:

                raise