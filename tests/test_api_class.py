import os
import requests
from dotenv import load_dotenv

load_dotenv()


class CloudLLM:
    """
    A reusable wrapper for sending masked prompts to OpenRouter
    and receiving masked responses.
    """

    def __init__(self, model="kwaipilot/kat-coder-pro:free"):
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = model
        self.headers = {
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://your-site.com",
            "X-Title": "AI Message Assistant"
        }

    def send_prompt(self, prompt: str) -> str:
        """
        Sends a masked RAG prompt to the LLM.
        Returns the response text OR error message.
        """

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        try:
            response = requests.post(self.url, headers=self.headers, json=payload)
            data = response.json()

            # Successful response
            if "choices" in data:
                return data["choices"][0]["message"]["content"]

            # Error case
            return f"API Error: {data}"

        except Exception as e:
            return f"Request Exception: {str(e)}"
