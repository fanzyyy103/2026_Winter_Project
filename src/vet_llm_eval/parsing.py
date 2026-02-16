import json
from typing import Dict, List

def normalize_label(x: str) -> str:
    s = (x or "").strip().lower()
    if s in {"abnormal", "positive", "pos", "1", "yes", "present"}:
        return "Abnormal"
    return "Normal"

def extract_json_object(text: str) -> str:
    if not text:
        return "{}"
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return "{}"
    return text[start:end+1]

def parse_llm_output(text: str, diseases: List[str]) -> Dict[str, str]:
    raw = extract_json_object(text)
    try:
        data = json.loads(raw)
        if not isinstance(data, dict):
            data = {}
    except Exception:
        data = {}

    result: Dict[str, str] = {}
    for d in diseases:
        result[d] = normalize_label(str(data.get(d, "Normal")))
    return result
