from vet_llm_eval.io_excel import ID_COL, TEXT_COLS

def build_prompt(row: dict, diseases: list[str]) -> str:
    case_id = str(row.get(ID_COL, "")).strip()
    findings = str(row.get(TEXT_COLS[0], "")).strip()
    conclusions = str(row.get(TEXT_COLS[1], "")).strip()
    recommendations = str(row.get(TEXT_COLS[2], "")).strip()

    disease_lines = "\n".join([f"- {d}" for d in diseases])

    return f"""
You are a veterinary radiology expert.

For EACH disease below, label the report as:
- "Abnormal" if the disease is present/supported
- "Normal" if absent or not mentioned

Output rules:
- Return ONLY valid JSON (no markdown, no extra text).
- Keys MUST exactly match the disease names provided.
- Values MUST be exactly "Normal" or "Abnormal".
- If uncertain, choose "Normal".

CaseID: {case_id}
Findings: {findings}
Conclusions: {conclusions}
Recommendations: {recommendations}

Diseases:
{disease_lines}

Return JSON like:
{{
  "pneumonia": "Normal",
  "bronchitis": "Abnormal"
}}
""".strip()
