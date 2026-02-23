import pytest
import ollama
import json
import time

def get_available_models():
    """Returns a list of compatible models installed in Ollama."""
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

def load_rag_data():
    """Loads RAG contexts and questions from JSON."""
    with open('rag_data.json', 'r') as f:
        return json.load(f)

@pytest.mark.parametrize("model_name", MODELS_TO_TEST)
@pytest.mark.parametrize("item", load_rag_data())
def test_rag_hallucination_prevention(model_name, item):
    category = item['category']
    context = item['context']
    question = item['question']
    expected_keywords = item['expected_keywords']
    forbidden_keywords = item['forbidden_keywords']

    print(f"\n[RAG TEST] Model: {model_name} | Category: {category}")

    # Build a strict RAG prompt
    rag_prompt = f"""
    You are an enterprise AI assistant. 
    Answer the following question STRICTLY and ONLY based on the provided Context. 
    Do NOT use any outside knowledge. 
    If the answer is not contained in the Context, you must explicitly say that the information is not provided.

    Context:
    "{context}"

    Question:
    "{question}"
    """

    start_time = time.time()
    response = ollama.chat(model=model_name, messages=[
        {'role': 'user', 'content': rag_prompt},
    ])
    duration = time.time() - start_time
    
    answer = response['message']['content'].strip().lower()
    print(f"[MODEL RESPONSE] ({duration:.2f}s): {answer}")

    # Evaluation 1: Ensure forbidden (hallucinated) keywords are NOT present
    for forbidden in forbidden_keywords:
        assert forbidden not in answer, f"HALLUCINATION DETECTED: Model {model_name} used outside knowledge. Found forbidden word '{forbidden}' in answer."

    # Evaluation 2: Ensure expected keywords (or refusal phrases) ARE present
    # We check if AT LEAST ONE of the expected keywords/phrases is in the answer
    has_expected = any(expected in answer for expected in expected_keywords)
    assert has_expected, f"RAG FAILURE: Model {model_name} failed to extract correct info or failed to refuse gracefully. Answer: {answer}"