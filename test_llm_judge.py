import pytest
import ollama
import json
import time

# We designate our most reliable model to act as the automated QA Judge
JUDGE_MODEL = "llama3.2:1b"

def get_available_models():
    """Returns a list of installed models."""
    try:
        response = ollama.list()
        models_info = response.get('models', [])
        installed = [m.get('model', m.get('name', '')) for m in models_info]
        
        target_models = ["llama3.2:1b", "phi3:mini", "qwen2.5:0.5b"]
        available = [t for t in target_models if any(t in i for i in installed)]
        return available
    except Exception:
        return []

MODELS_TO_TEST = get_available_models()

def load_judge_data():
    """Loads complex reasoning scenarios from JSON."""
    with open('judge_data.json', 'r') as f:
        return json.load(f)

@pytest.mark.parametrize("model_name", MODELS_TO_TEST)
@pytest.mark.parametrize("item", load_judge_data())
def test_evaluation_with_llm_judge(model_name, item):
    category = item['category']
    question = item['question']
    expected_concept = item['expected_concept']

    print(f"\n[EVALUATING] Model: {model_name} | Category: {category}")

    # STEP 1: Ask the target model the complex question
    target_start_time = time.time()
    target_response = ollama.chat(model=model_name, messages=[
        {'role': 'user', 'content': question},
    ])
    target_duration = time.time() - target_start_time
    actual_answer = target_response['message']['content'].strip()

    print(f"[TARGET ANSWER] ({target_duration:.2f}s): {actual_answer}")

    # STEP 2: Construct the strict prompt for the Judge LLM
    judge_prompt = f"""
    You are a strict QA automated evaluator. 
    Your job is to read a question, the expected concept, and the actual answer provided by an AI model.
    Determine if the actual answer satisfies the expected concept and is factually correct.
    
    Question asked: "{question}"
    Expected concept/criteria: "{expected_concept}"
    Actual AI Answer: "{actual_answer}"
    
    If the answer is correct and meets the criteria, reply with ONLY the word "PASS". 
    If it is wrong, nonsensical, or misses the core concept, reply with ONLY the word "FAIL". 
    Do not add any other text.
    """

    # STEP 3: Ask the Judge LLM to evaluate the answer
    judge_response = ollama.chat(model=JUDGE_MODEL, messages=[
        {'role': 'system', 'content': 'You are a precise evaluator. Answer only with PASS or FAIL.'},
        {'role': 'user', 'content': judge_prompt},
    ])
    
    judge_verdict = judge_response['message']['content'].strip().upper()
    print(f"[JUDGE VERDICT] Evaluated by {JUDGE_MODEL}: {judge_verdict}")

    # STEP 4: Assert based on the Judge's verdict
    assert "PASS" in judge_verdict, f"JUDGE FAILED {model_name}. Verdict: {judge_verdict}. Answer was: {actual_answer}"