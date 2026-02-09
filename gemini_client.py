import os
import google.generativeai as genai
from typing import List

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = genai.GenerativeModel("gemini-2.5-flash")


def batch_prompts(prompts: List[str], batch_size: int = 5) -> List[str]:
    """Batch Gemini calls to reduce token usage."""
    results = []

    for i in range(0, len(prompts), batch_size):
        batch = prompts[i:i + batch_size]
        joined_prompt = "\n".join(
            f"{idx+1}. {p}" for idx, p in enumerate(batch)
        )

        response = MODEL.generate_content(
            f"Process the following items and respond line-by-line:\n{joined_prompt}"
        )

        results.extend(response.text.splitlines())

    return results
