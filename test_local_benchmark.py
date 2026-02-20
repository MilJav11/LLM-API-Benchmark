import pytest
import ollama
import time
import json

# Smart model detection: Only test models that are actually installed
def get_available_models():
    installed = [m['name'] for m in ollama.list()['models']]
    # Filter only models we are interested in
    target_models = ["llama3.2:1b", "phi3:mini", "qwen2.5:0.5b"]
    return [m for m in target_models if m in installed or m + ":latest" in installed]

MODELS_TO_TEST = get_available_models()

# Helper function to load test data
def load_test_data():
    with open('benchmark_data.json', 'r') as f:
        return json.load(f)

# Double parametrization: 3 models x 3 questions = 9 tests!
@pytest.mark.parametrize("model_name", MODELS_TO_TEST)
@pytest.mark.parametrize("item", load_test_data())
def test_model_speed_and_accuracy(model_name, item):
    category = item['category']
    question = item['question']
    expected_list = item['expected'] 
    
    print(f"\n[START] Model: {model_name} | Category: {category}")
    
    # Start the timer
    start_time = time.time()
    
    # Call the specific model via Ollama
    response = ollama.chat(model=model_name, messages=[
        {'role': 'user', 'content': f"Answer with one word only. {question}"},
    ])
    
    # Stop the timer
    duration = time.time() - start_time
    
    # Clean the response
    answer = response['message']['content'].lower().strip().replace(".", "")
    
    # Print execution report
    print(f"[RESULT] Time: {duration:.2f}s | Answer: '{answer}'")
    
    # Verify if AT LEAST ONE of the expected words is in the answer
    success = any(expected in answer for expected in expected_list)
    
    assert success, f"FAILURE: {model_name} failed on {category}. Got: '{answer}'"