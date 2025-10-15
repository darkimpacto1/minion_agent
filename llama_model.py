from typing import List, Dict
import os
import ollama
from ollama import ChatResponse

#Ensure GPU usage is enabled
os.environ["OLLAMA_USE_CUDA"] = "1"  # This enables CUDA

def chat_with_llama(prompt: str, history: List[Dict[str, str]] = None) -> str:
    messages = history if history else []
    messages.append({"role": "user", "content": prompt})

    response: ChatResponse = ollama.chat(
        model="llama3",
        messages=messages
    )
    return response['message']['content']
