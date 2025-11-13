# Nemosine PoC – Mentor + LLM num arquivo só (versão simples)
import sys
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

OUT = Path("data/outputs")
OUT.mkdir(parents=True, exist_ok=True)
LOG = OUT / "logs.jsonl"


def enviar_para_llm(mensagem: str) -> str:
    """Chama ChatGPT de forma simples. Se der algo errado, devolve texto explicando."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-5")

    if not api_key:
        return "(LLM off) Falta OPENAI_API_KEY no .env na raiz do projeto."

    client = OpenAI(api_key=api_key)

    try:
        resp = client.responses.create(model=model, input=mensagem)
        return getattr(resp, "output_text", "(LLM) resposta sem output_text")
    except Exception as e:
        return f"(LLM erro) {e.__class__.__name__}: {e}"


def mentor_responde(pedido: str) -> str:
    t = pedido.lower()
    if "passo" in t or "hoje" in t or "agora" in t:
        return "Passo único de hoje: rodar este menu e ver o LLM respondendo ao seu pedido."
    if "api" in t:
        return "A API já está integrada neste arquivo. Se der erro, será mostrado no texto do LLM."
    return "Sugestão: escreva o que você quer que o Nemosine faça agora em uma frase clara."


print("Nemosine PoC (Desktop) ativo.")
pedido = input("Diga ao Mentor o que você quer agora:\n> ").strip() or "quero um passo concreto pra hoje"

mensagem = mentor_responde(pedido)
eco_llm = enviar_para_llm(pedido)

registro = {
    "persona": "Mentor",
    "lugar_do_atlas": "Núcleo",
    "mensagem": mensagem,
    "rastro": {"fonte": "Mentor", "coerencia": 0.9, "referencias": []},
    "pedido": pedido,
    "llm_echo": eco_llm,
}

with LOG.open("a", encoding="utf-8") as f:
    f.write(json.dumps(registro, ensure_ascii=False) + "\n")

print("Mentor:", mensagem)

try:
    # tenta imprimir normalmente
   try:
    print("LLM :", eco_llm.encode("utf-8").decode("utf-8"))
except:
    safe = eco_llm.encode("ascii", "replace").decode("ascii")
    print("LLM :", safe)
    print("[Aviso] O console do Windows não suporta alguns caracteres Unicode.")
    print("[Aviso] A resposta COMPLETA está salva em data/outputs/logs.jsonl.")

print("✅ Registrado em data/outputs/logs.jsonl")


