from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tiktoken
import requests

# 1. Initialize FastAPI with metadata for the Swagger UI
app = FastAPI(
    title="Agentic Prompt Optimizer", 
    description="An AI agent that compresses user prompts to save LLM token costs.",
    version="1.0.0"
)

# 2. What the recruiter/user will send
class PromptRequest(BaseModel):
    raw_prompt: str
    target_max_tokens: int = 50

# 3. What your API will return
class PromptResponse(BaseModel):
    optimized_prompt: str
    original_token_count: int
    new_token_count: int
    compression_ratio: str
    success: bool

# 4. Build the Agent's Tool (Token Counter)
def count_tokens(text: str) -> int:
    """Utility tool to calculate token usage."""
    # cl100k_base is the standard encoding for modern LLMs
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

# 5. Write the Agentic Endpoint
@app.post("/api/v1/optimize", response_model=PromptResponse)
async def optimize_prompt(request: PromptRequest):
    orig_tokens = count_tokens(request.raw_prompt)
    
    # The Agent's Persona and Rules
    system_instruction = (
        "You are an expert AI prompt engineer. "
        f"Compress the following prompt to be under {request.target_max_tokens} tokens. "
        "Remove filler words but keep the exact core intent, variables, and instructions. "
        "Output ONLY the compressed prompt, nothing else."
    )
    
    # The payload to send to your local Ollama instance
    ollama_payload = {
        "model": "llama3.2", # Make sure this matches the model you downloaded
        "prompt": f"{system_instruction}\n\nOriginal Prompt: {request.raw_prompt}",
        "stream": False
    }
    
    try:
        # Call the local LLM asynchronously
        response = requests.post("http://localhost:11434/api/generate", json=ollama_payload)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=503, detail="Local LLM engine is offline or unreachable.")
        
    # Extract and clean the AI's response
    optimized_text = response.json().get("response", "").strip()
    new_tokens = count_tokens(optimized_text)
    
    # Calculate business value (compression ratio)
    ratio = round((1 - (new_tokens / orig_tokens)) * 100, 1) if orig_tokens > 0 else 0
    
    return PromptResponse(
        optimized_prompt=optimized_text,
        original_token_count=orig_tokens,
        new_token_count=new_tokens,
        compression_ratio=f"{ratio}% smaller",
        success=new_tokens <= request.target_max_tokens
    )