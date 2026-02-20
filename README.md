[![LLM Benchmark CI](https://github.com/MilJav11/LLM-API-Benchmark/actions/workflows/main.yml/badge.svg)](https://github.com/MilJav11/LLM-API-Benchmark/actions/workflows/main.yml)

# LLM Local API Benchmark 🚀

Professional QA framework for benchmarking local LLMs (Llama 3.2, Phi-3, Qwen 2.5) using **Ollama** and **Pytest**.

## 📊 Overview

This project measures **inference latency** and **instruction-following accuracy** on local hardware. It automates the process of sending prompts to multiple models and validating their responses against expected criteria.

### Key Results

| Model             | Avg. Time | Status    | Note                                |
| :---------------- | :-------- | :-------- | :---------------------------------- |
| **Llama 3.2:1b**  | ~11s      | ✅ Passed | Very stable and consistent.         |
| **Phi-3:mini**    | ~19s      | ✅ Passed | High quality but talkative.         |
| **Qwen 2.5:0.5b** | **~4s**   | ❌ Failed | Fast, but failed strict logic task. |

## 📁 Reports

The benchmark generates automated reports in two formats for easy analysis:

- 🌐 **[HTML Report (Interactive)](./benchmark_report.html)** - Detailed view with duration and error logs.
- 📄 **[PDF Report (Static)](./benchmark_report.pdf)** - Print-ready version of the test results.

## 🛠️ Tech Stack

- **Python 3.12** & **Pytest** - Core testing logic.
- **Ollama** - Local LLM inference engine.
- **pytest-html** - Automated reporting plugin.
- **JSON** - Structured test data management.

## 🔍 QA Insights

During testing, we discovered that **Qwen 2.5:0.5b** has issues following strict "one-word" constraints in logical tasks, often echoing the question or adding context. **Llama 3.2:1b** provides the best balance between speed and reliability.

## 🚀 Scalability & Adding New Models

This framework is designed to be easily extensible. To add a new model to the benchmark, follow these steps:

#### Step 1: Download the model

Use Ollama to pull your desired model (e.g., Mistral or Gemma):

```bash
ollama pull mistral

Step 2: Update the test script
Add the new model name to the MODELS_TO_TEST list in test_local_benchmark.py:

Python
MODELS_TO_TEST = ["llama3.2:1b", "phi3:mini", "qwen2.5:0.5b", "mistral"]

Step 3: Expand test data (Optional)
Add more complex scenarios to benchmark_data.json to challenge the new model's capabilities.

---
```
