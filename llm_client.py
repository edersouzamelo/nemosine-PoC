# Nemosine PoC – LLM Client (real, lendo .env)
import os
from typing import Optional
try:
    from dotenv import load_dotenv
    from openai import OpenAI
except Exception:
    load_dotenv = None
    OpenAI = None

def enviar_para_llm(mensagem: str) -> str:
    """Envia texto para ChatGPT. Se faltar lib/chave, devolve aviso claro."""
    if load_dotenv:
        load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-5")

    if not OpenAI:
        return "(LLM off) Instale as libs: pip install openai python-dotenv"
    if not api_key:
        return "(LLM off) Falta OPENAI_API_KEY no arquivo .env (raiz do projeto)."

    client = OpenAI(api_key=api_key)
    try:
        resp = client.responses.create(model=model, input=mensagem)
        return getattr(resp, "output_text", "(LLM) sem output_text")
    except Exception as e:
        return f"(LLM erro) {e.__class__.__name__}: {e}"
