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




#### save code :

git add .
git commit -m "save file contents"
git push