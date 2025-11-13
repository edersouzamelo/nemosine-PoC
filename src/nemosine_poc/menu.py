# -*- coding: utf-8 -*-
"""Nemosine PoC – Mentor + LLM num arquivo só (versão simples)."""

from __future__ import annotations

import sys
sys.stdout.reconfigure(encoding="utf-8")

from pathlib import Path
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

# Pasta e arquivo de log
OUT = Path("data/outputs")
OUT.mkdir(parents=True, exist_ok=True)
LOG = OUT / "logs.jsonl"


def safe_print(prefixo: str, texto: str) -> None:
    """
    Imprime texto de forma segura em consoles que não suportam Unicode completo.
    Se der UnicodeEncodeError, converte para ASCII com substituição e avisa.
    """
    try:
        print(prefixo, texto)
    except UnicodeEncodeError:
        texto_seguro = texto.encode("ascii", errors="replace").decode("ascii")
        print(prefixo, texto_seguro)
        print("[Aviso] Console do Windows não suporta todos os caracteres Unicode.")
        print("[Aviso] Resposta COMPLETA está em data/outputs/logs.jsonl.")


def enviar_para_llm(pedido: str) -> str:
    """
    Chama ChatGPT de forma simples.
    Qualquer erro vira texto e volta para o menu.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-5")

    if not api_key:
        return "(LLM off) Falta OPENAI_API_KEY no .env na raiz do projeto."

    client = OpenAI(api_key=api_key)

    try:
        resp = client.responses.create(
            model=model,
            input=pedido,
        )
        # SDK novo expõe isso em output_text; se não tiver, converte o objeto todo.
        if hasattr(resp, "output_text"):
            return resp.output_text
        return str(resp)
    except Exception as e:
        try:
            msg = str(e)
        except Exception:
            msg = repr(e)
        return f"(LLM erro) {e.__class__.__name__}: {msg}"


def mentor_responde(pedido: str) -> str:
    """
    Regrinha simples do Mentor para responder ao pedido.
    """
    t = pedido.lower()

    if "passo" in t or "hoje" in t or "agora" in t:
        return "Passo único de hoje: rodar este menu e ver o LLM respondendo ao seu pedido."

    if "api" in t:
        return "A API já está integrada neste arquivo. Se der erro, o texto do LLM vai explicar."

    return "Sugestão: escreva o que você quer que o Nemosine faça agora em uma frase clara."


def main() -> None:
    print("Nemosine PoC (Desktop) ativo.")

    pedido = input("Diga ao Mentor o que você quer agora:\n> ").strip()
    if not pedido:
        pedido = "quero um passo concreto pra hoje"

    mensagem = mentor_responde(pedido)
    eco_llm = enviar_para_llm(pedido)

    registro = {
        "persona": "Mentor",
        "lugar_do_atlas": "Núcleo",
        "mensagem": mensagem,
        "rastro": {
            "fonte": "Mentor",
            "coerencia": 0.9,
            "referencias": [],
        },
        "pedido": pedido,
        "llm_echo": eco_llm,
    }

    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")

    print("Mentor:", mensagem)
    safe_print("LLM :", eco_llm)
    print("✅ Registrado em data/outputs/logs.jsonl")


if __name__ == "__main__":
    main()

