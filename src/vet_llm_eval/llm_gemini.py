import os
from typing import List
import google.generativeai as genai

class GeminiClient:
    def __init__(self, model: str):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Missing GEMINI_API_KEY. Put it in your environment or .env file.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def generate_one(self, prompt: str) -> str:
        resp = self.model.generate_content(prompt)
        return resp.text or ""

    def generate_batch(self, prompts: List[str], batch_size: int) -> List[str]:
        outputs: List[str] = []
        for i in range(0, len(prompts), batch_size):
            chunk = prompts[i:i + batch_size]
            for p in chunk:
                outputs.append(self.generate_one(p))
        return outputs
