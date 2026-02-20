# LLM Local API Benchmark 🚀

Professional QA framework for benchmarking local LLMs (Llama 3.2, Phi-3, Qwen 2.5) using **Ollama** and **Pytest**.

## 📊 Overview
This project measures **inference latency** and **instruction-following accuracy** on local hardware.

### Key Results
| Model | Avg. Time | Status | Note |
| :--- | :--- | :--- | :--- |
| **Llama 3.2:1b** | ~11s | ✅ Passed | Very stable and consistent. |
| **Phi-3:mini** | ~19s | ✅ Passed | High quality but talkative. |
| **Qwen 2.5:0.5b** | **~4s** | ❌ Failed | Fast, but failed strict logic task. |

## 📁 Reports
The benchmark generates automated reports in two formats:
* 🌐 [HTML Report (Interactive)](./benchmark_report.html)
* 📄 [PDF Report (Static)](./benchmark_report.pdf)

## 🛠️ Tech Stack
* **Python 3.12** & **Pytest**
* **Ollama** (Local Inference)
* **pytest-html** (Reporting)

## 🔍 QA Insights
During testing, we discovered that **Qwen 2.5:0.5b** has issues following strict "one-word" constraints in logical tasks, while **Llama 3.2:1b** provides the best balance between speed and reliability.
