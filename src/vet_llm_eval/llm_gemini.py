from __future__ import annotations
import os
from typing import List
import time
from dotenv import load_dotenv

from google import genai


class GeminiClient:
    def __init__(self, model: str):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Missing GEMINI_API_KEY in environment/.env")

        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate_one(self, prompt: str) -> str:
        resp = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        
        return getattr(resp, "text", "") or ""
    def generate_batch(self, prompts: List[str], batch_size: int) -> List[str]:
        outputs: List[str] = []
        INTER_CALL_DELAY = 2

        for i in range(0, len(prompts), batch_size):
            chunk = prompts[i : i + batch_size]

            for p in chunk:
                outputs.append(self.generate_one(p))
                time.sleep(INTER_CALL_DELAY)

        return outputs