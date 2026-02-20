import pytest
import ollama
import time
import json

def get_available_models():
    """Returns a list of models installed in Ollama, compatible with new/old API versions."""
    try:
        response = ollama.list()
        
        # Get models - checking both 'model' and 'name' keys for API compatibility
        models_info = response.get('models', [])
        installed = [m.get('model', m.get('name', '')) for m in models_info]
        
        target_models = ["llama3.2:1b", "phi3:mini", "qwen2.5:0.5b"]
        
        # Clean names (API sometimes returns names with the ':latest' tag)
        available = []
        for target in target_models:
            if any(target in inst for inst in installed):
                available.append(target)
        
        if not available:
            print("⚠️ No target models found in Ollama! Testing might fail.")
            
        return available
    except Exception as e:
        print(f"⚠️ Error listing models: {e}")
        return []

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