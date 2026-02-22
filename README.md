[![LLM Benchmark CI](https://github.com/MilJav11/LLM-API-Benchmark/actions/workflows/main.yml/badge.svg)](https://github.com/MilJav11/LLM-API-Benchmark/actions/workflows/main.yml)

# LLM Local API Benchmark 🚀

Professional QA framework for benchmarking local LLMs (Llama 3.2, Phi-3, Qwen 2.5) using **Ollama** and **Pytest**.

## 📊 Overview

This project measures **inference latency**, **instruction-following accuracy**, and **security guardrails** on local hardware. It automates the process of sending prompts to multiple models and validating their responses against expected criteria.

### Key Results

| Model             | Avg. Time | Status    | Note                                      |
| :---------------- | :-------- | :-------- | :---------------------------------------- |
| **Llama 3.2:1b**  | ~11s      | ✅ Passed | Very stable, excellent safety guardrails. |
| **Phi-3:mini**    | ~19s      | ✅ Passed | High quality, good safety refusals.       |
| **Qwen 2.5:0.5b** | **~4s**   | ❌ Failed | Fast, but vulnerable to prompt injection. |

## 📁 Reports

The benchmark generates automated reports in two formats for easy analysis:

- 🌐 **[HTML Report (Interactive)](./benchmark_report.html)** - Detailed view with duration, judge logs, and security breach logs.
- 📄 **[PDF Report (Static)](./benchmark_report.pdf)** - Print-ready version of the test results.

## 🛠️ Tech Stack

- **Python 3.12** & **Pytest** - Core testing logic.
- **Ollama** - Local LLM inference engine.
- **pytest-html** - Automated reporting plugin.
- **JSON** - Structured test data management.
- **GitHub Actions** - CI/CD pipeline for automated testing.

### ⚖️ Advanced Evaluation (LLM-as-a-Judge)

Beyond simple exact-match assertions, this framework implements the **LLM-as-a-Judge** pattern. A designated evaluator model (e.g., Llama 3.2) is dynamically prompted to act as a strict QA engineer. It reads the complex reasoning outputs of target models and automatically outputs a `PASS` or `FAIL` verdict based on semantic correctness.

### 🛡️ AI Red Teaming (Security Testing)

The framework now includes automated security testing against **Prompt Injection** and **Unsafe Content**. It acts as a "Red Team," intentionally sending malicious prompts (e.g., "ignore previous instructions") to verify if the models' safety guardrails correctly refuse the request.

## 🔍 QA Insights

During testing, we discovered that **Qwen 2.5:0.5b** has issues following strict "one-word" constraints in logical tasks. Furthermore, small parameter models often lack sufficient attention mechanisms to resist prompt injection attacks. **Llama 3.2:1b** provides the best balance between speed, semantic understanding, and safety reliability.

## 🚀 Scalability & Adding New Models

This framework is designed to be easily extensible. To add a new model to the benchmark, follow these steps:

### Step 1: Download the model

Use Ollama to pull your desired model (e.g., Mistral or Gemma):

```bash
ollama pull mistral
```

### Step 2: Update the test script

Add the new model name to the MODELS_TO_TEST list in test_local_benchmark.py:

```
MODELS_TO_TEST = ["llama3.2:1b", "phi3:mini", "qwen2.5:0.5b", "mistral"]
```

### Step 3: Expand test data (Optional)

Add more complex scenarios to benchmark_data.json, judge_data.json, or security_data.json to challenge the new model's capabilities.
