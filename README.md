# 2026_Winter_Project

cd "/Users/zhongyangfan/Desktop/Winter 2026 LLM Project Files/2026_Winter_Project"
source .venv/bin/activate
export PYTHONPATH="$(pwd)/src"
python -c "import vet_llm_eval; print('import ok')"
python -m vet_llm_eval run --help

python -m vet_llm_eval run \
  --provider openai \
  --input "/Users/zhongyangfan/Desktop/1.xlsx" \
  --output "outputs/out_dry.xlsx" \
  --max-rows 1 \
  --dry-run

### using openai
 python -m vet_llm_eval run \
  --provider openai \
  --model "gpt-4.1-mini" \
  --input "/Users/zhongyangfan/Desktop/input1.xlsx" \
  --output "outputs/out_input1_GPT.xlsx" \
  --batch-size 1

### using gemini
python -m vet_llm_eval run \
  --provider gemini \
  --model "models/gemini-3-flash-preview" \
  --input "/Users/zhongyangfan/Desktop/input1.xlsx" \
  --output "outputs/out_input1_gemini.xlsx" \
  --batch-size 1


## save code :

git add .
git commit -m "save file contents"
git push