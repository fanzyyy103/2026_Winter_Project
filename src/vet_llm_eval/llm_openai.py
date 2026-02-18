from __future__ import annotations
from typing import List
from dotenv import load_dotenv
import os
from openai import OpenAI

class OpenAIClient:
    def __init__(self, model: str):
        load_dotenv()
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("Missing OPENAI_API_KEY in environment/.env")
        self.client = OpenAI()
        self.model = model

    def generate_one(self, prompt: str) -> str:
        resp = self.client.responses.create(
            model=self.model,
            input=prompt,
        )
        return resp.output_text or ""

    def generate_batch(self, prompts: List[str], batch_size: int) -> List[str]:
        outputs: List[str] = []
        for i in range(0, len(prompts), batch_size):
            chunk = prompts[i:i + batch_size]
            for p in chunk:
                outputs.append(self.generate_one(p))
        return outputs
