import os
import google.generativeai as genai
from typing import List

# start add API and the model we want to use
genai.configure(api_key="AIzaSyA4R423SEz9XZ7OoP0DGgKve_bAxEAN1EM")

MODEL = genai.GenerativeModel("gemini-1.5-flash")


def batch_prompts(prompts: List[str], batch_size: int = 5) -> List[str]:
    # store all the batches results
    results = []
    
    #traverse all the batches based on our prompts
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
