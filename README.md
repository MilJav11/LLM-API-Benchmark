# LLM Local API Benchmark 🚀

Professional QA framework for benchmarking local LLMs (Llama 3.2, Phi-3, Qwen 2.5) using **Ollama** and **Pytest**.

## 📊 Overview

This project measures **inference latency** and **instruction-following accuracy** on local hardware.

### Key Results

| Model             | Avg. Time | Status    | Note                                |
| :---------------- | :-------- | :-------- | :---------------------------------- |
| **Llama 3.2:1b**  | ~11s      | ✅ Passed | Very stable and consistent.         |
| **Phi-3:mini**    | ~19s      | ✅ Passed | High quality but talkative.         |
| **Qwen 2.5:0.5b** | **~4s**   | ❌ Failed | Fast, but failed strict logic task. |

## 📁 Reports

The benchmark generates automated reports in two formats:

- 🌐 [HTML Report (Interactive)](./benchmark_report.html)
- 📄 [PDF Report (Static)](./benchmark_report.pdf)

## 🛠️ Tech Stack

- **Python 3.12** & **Pytest**
- **Ollama** (Local Inference)
- **pytest-html** (Reporting)

## 🔍 QA Insights

During testing, we discovered that **Qwen 2.5:0.5b** has issues following strict "one-word" constraints in logical tasks, while **Llama 3.2:1b** provides the best balance between speed and reliability.

## 🚀 Scalability & Adding New Models

This framework is designed to be easily extensible. To add a new model to the benchmark, follow these three simple steps:

1. **Download the model:** Use Ollama to pull your desired model (e.g., Mistral or Gemma):
   ```powershell
   ollama pull mistral
   ```

2.Update the test script: Add the new model name to the MODELS_TO_TEST list
in test_local_benchmark.py:

MODELS_TO_TEST = ["llama3.2:1b", "phi3:mini", "qwen2.5:0.5b", "mistral"]

3. Expand test data (Optional): Add more complex scenarios to benchmark_data.json to challenge the new model's capabilities.
