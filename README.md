# Agentic Prompt Optimizer

A lightweight, FastAPI-based microservice that utilizes a local Large Language Model (LLM) to autonomously compress user prompts. This tool reduces token consumption (and associated API costs) by trimming filler words while preserving the core intent, instructions, and variables of the original prompt.

## Key Features

* **Local AI Execution:** Integrates with Ollama for zero-cost, local LLM inference.
* **Token Tracking:** Uses OpenAI's `tiktoken` (`cl100k_base` encoding) to calculate exact token usage before and after compression.
* **Business Metrics:** Automatically calculates and returns the compression ratio (e.g., "66.7% smaller") to quantify token savings.
* **FastAPI Backend:** Built with asynchronous Python, strict Pydantic schemas, and built-in Swagger UI documentation.

## Tech Stack

* **Framework:** FastAPI, Uvicorn
* **AI/LLM:** Ollama (Llama 3.2)
* **Tokenization:** Tiktoken
* **Language:** Python 3.x

## Prerequisites

* Python 3.8+ installed on your machine.
* [Ollama](https://ollama.com/) installed and running locally.

## Local Setup & Installation

1. **Clone the repository and navigate to the project directory:**
```bash
git clone <your-github-repo-url>
cd PromptOptimiser

```


2. **Create and activate a virtual environment:**
```powershell
python -m venv poenv
.\poenv\Scripts\Activate.ps1

```


3. **Install the required dependencies:**
```powershell
pip install fastapi uvicorn tiktoken requests pydantic

```



## Running the Application

1. **Start the local LLM engine:**
Open a separate terminal and run:
```bash
ollama run llama3.2

```


2. **Start the FastAPI server:**
In your active virtual environment terminal, run the application as a Python module (bypasses Windows execution policies):
```powershell
python -m uvicorn main:app --reload

```


3. **Access the UI:**
Open your browser and navigate to the Swagger UI dashboard at: `[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)`

## API Usage Example

**Endpoint:** `POST /api/v1/optimize`

**Request Body:**

```json
{
  "raw_prompt": "Can you please help me write a very long and detailed email to my boss asking him for a vacation next week starting on Monday because I really need to take some time off to relax and go to the mountains?",
  "target_max_tokens": 20
}

```

**Response:**

```json
{
  "optimized_prompt": "Write a detailed email to boss requesting a Monday start vacation next week.",
  "original_token_count": 42,
  "new_token_count": 14,
  "compression_ratio": "66.7% smaller",
  "success": true
}

```

## Future Enhancements

* **Autonomous Retry Loop:** Implement agentic logic to automatically re-prompt the LLM if the initial compression does not meet the target token count.
* **Cloud Deployment:** Containerize the application using Docker and deploy to Azure Container Apps, integrating Azure Key Vault for secure environment variable management.

---

Are you ready to initialize the Git repository for this and push it up to your GitHub, or would you prefer to build out the autonomous retry loop next?
