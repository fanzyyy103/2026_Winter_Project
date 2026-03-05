from vet_llm_eval.io_excel import ID_COL, TEXT_COLS

def build_prompt(row: dict, diseases: list[str]) -> str:
    case_id = str(row.get(ID_COL, "")).strip()
    findings = str(row.get(TEXT_COLS[0], "")).strip()
    conclusions = str(row.get(TEXT_COLS[1], "")).strip()
    recommendations = str(row.get(TEXT_COLS[2], "")).strip()

    disease_lines = "\n".join([f"- {d}" for d in diseases])

    return f"""
You are a veterinary radiology expert.

Your task is to review the radiology report and determine whether each disease is present.

For EACH disease below, label the report as:

* "Abnormal" if the disease is present or supported by the report
* "Normal" if the disease is absent or not mentioned

Use the definitions below to help interpret the findings.

Output rules:

* Return ONLY valid JSON (no markdown, no explanations).
* Keys MUST exactly match the disease names.
* Values MUST be exactly "Normal" or "Abnormal".
* If uncertain, choose "Normal".

CaseID: {case_id}

Findings: {findings}

Conclusions: {conclusions}

Recommendations: {recommendations}

ATTENTION:
* ONLY label "Abnormal" when the report clearly supports the disease.
* Do not infer diseases without evidence.

Diseases and Definitions:

bronchiectasis — permanent dilation and thickening of the bronchi caused by chronic inflammation or infection.

bronchitis — inflammation of the bronchial airways, often associated with bronchial wall thickening and increased mucus.

cardiomegaly — abnormal enlargement of the heart.

diseased_lungs — general evidence of abnormal lung tissue or pulmonary pathology.

esophagitis — inflammation of the esophagus.

focal_caudodorsal_lung — localized abnormality in the caudal (rear) and dorsal (upper) lung region.

focal_perihilar — localized abnormality near the lung hilum where bronchi and vessels enter the lungs.

hypo_plastic_trachea — congenital narrowing of the trachea due to underdevelopment.

interstitial — increased density or thickening of lung interstitial tissue.

left_sided_cardiomegaly — enlargement of the left atrium or left ventricle.

pericardial_effusion — accumulation of fluid within the pericardial sac surrounding the heart.

perihilar_infiltrate — abnormal material (inflammation, fluid, or cells) around the lung hilum.

pleural_effusion — abnormal fluid accumulation in the pleural space surrounding the lungs.

pneumonia — infection or inflammation of the lung parenchyma causing consolidation.

pulmonary_hypoinflation — reduced lung inflation or decreased lung volume.

pulmonary_nodules — small rounded masses within lung tissue.

pulmonary_vessel_enlargement — abnormal dilation or prominence of pulmonary blood vessels.

right_sided_cardiomegaly — enlargement of the right atrium or right ventricle.

rtm — abnormalities affecting the right middle lung lobe.

thoracic_lymphadenopathy — enlargement of lymph nodes within the thoracic cavity.

Return JSON like:

{{
"bronchiectasis": "Normal",
"bronchitis": "Normal",
"cardiomegaly": "Normal",
"diseased_lungs": "Normal",
"esophagitis": "Normal",
"focal_caudodorsal_lung": "Normal",
"focal_perihilar": "Normal",
"hypo_plastic_trachea": "Normal",
"interstitial": "Normal",
"left_sided_cardiomegaly": "Normal",
"pericardial_effusion": "Normal",
"perihilar_infiltrate": "Normal",
"pleural_effusion": "Normal",
"pneumonia": "Normal",
"pulmonary_hypoinflation": "Normal",
"pulmonary_nodules": "Normal",
"pulmonary_vessel_enlargement": "Normal",
"right_sided_cardiomegaly": "Normal",
"rtm": "Normal",
"thoracic_lymphadenopathy": "Normal"
}}

""".strip()
