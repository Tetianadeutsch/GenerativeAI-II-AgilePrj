# utils/llm_utils.py

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import HuggingFaceHub

load_dotenv()

# Cache LLM globally
_cached_llm = None
USE_HF = False  # Flag to track fallback

def get_llm(force_hf: bool = False):
    global _cached_llm, USE_HF

    if _cached_llm is not None and not force_hf:
        return _cached_llm

    if force_hf or USE_HF:
        print("⚠️ Using Hugging Face fallback")
        _cached_llm = HuggingFaceHub(
            repo_id="google/flan-t5-base",
            model_kwargs={"temperature": 0.3, "max_length": 512}
        )
        return _cached_llm

    try:
        if os.getenv("GOOGLE_API_KEY"):
            print("✅ Using Gemini Flash")
            _cached_llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
            return _cached_llm
        else:
            raise ValueError("No GOOGLE_API_KEY")
    except Exception as e:
        print(f"⚠️ Gemini failed: {e}")
        USE_HF = True
        return get_llm(force_hf=True)


