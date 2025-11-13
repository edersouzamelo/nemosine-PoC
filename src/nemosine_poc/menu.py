#!/usr/bin/env python3
# Nemosine PoC – Mentor + LLM num arquivo só (versão simples)

import sys
from pathlib import Path
import json
import os

from dotenv import load_dotenv
from openai import OpenAI


# -------------------------------------------------------------------
# Configuração de saída e paths
# -------------------------------------------------------------------

# Tenta garantir que o console aceite UTF-8 (quando possível)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Pasta de logs (mesmo esquema de antes)
OUT = Path("data/outputs")
OUT.mkdir(parents=True, exist_ok=True)
LOG = OUT / "logs.jsonl"


# -------------------------------------------------------------------
# Função que chama o LLM de forma simples
# -------------------------------------------------------------------

def enviar_para_llm(pedido: str) -> str:
    """
    Chama ChatGPT usando chat.completions.
    Se der qualquer erro, devolve texto explicando.
    """
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        return "(LLM off) Falta OPENAI_API_KEY no .env na raiz do projeto."

    client = OpenAI(api_key=api_key)

    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é o Mentor do Sistema Nemosine Nous em modo PoC Desktop. "
                        "Responda de forma clara, curta e em português do Brasil."
                    ),
                },
                {
                    "role": "user",
                    "content": pedido,
                },
            ],
        )

        # pega o texto da resposta
        msg = resp.choices[0].message
        texto = msg.content or ""
        return texto

    except UnicodeEncodeError as e:
        # Caso o bug de Unicode venha de dentro da lib
        return f"(LLM erro de unicode dentro da lib OpenAI: {e})"
    except Exception as e:
        return f"(LLM erro) {e.__class__.__name__}: {e}"


# -------------------------------------------------------------------
# Mentor local (regra simples)
# -------------------------------------------------------------------

def mentor_responde_local(pedido: str) -> str:
    t = pedido.lower()
    if "passo" in t or "hoje" in t or "agora" in t:
        return "Passo único de hoje: rodar este menu e ver o LLM respondendo ao seu pedido."
    if "api" in t:
        return "A API já está integrada neste arquivo. Se der erro, ele aparece no texto da linha 'LLM :'."
    return "Sugestão: escreva o que você quer que o Nemosine faça agora em uma frase clara."


# -------------------------------------------------------------------
# Utilidades: log + impressão segura
# -------------------------------------------------------------------

def salvar_log(registro: dict) -> None:
    try:
        with LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(registro, ensure_ascii=False) + "\n")
    except Exception:
        # se o log falhar, não quebra o programa
        pass


def imprimir_seguro(prefixo: str, texto: str) -> None:
    try:
        print(prefixo, texto)
    except UnicodeEncodeError:
        seguro = texto.encode("ascii", "replace").decode("ascii")
        print(prefixo, seguro)
        print("[Aviso] O console do Windows não mostrou todos os caracteres Unicode.")
        print("[Aviso] A resposta COMPLETA está salva em data/outputs/logs.jsonl.")


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

def main() -> None:
    print("Nemosine PoC (Desktop) ativo.")

    pedido = input("Diga ao Mentor o que você quer agora:\n> ").strip()
    if not pedido:
        pedido = "quero um passo concreto pra hoje"

    resposta_mentor = mentor_responde_local(pedido)
    resposta_llm = enviar_para_llm(pedido)

    registro = {
        "persona": "Mentor",
        "lugar_do_atlas": "Núcleo",
        "pedido": pedido,
        "mensagem_mentor": resposta_mentor,
        "resposta_llm": resposta_llm,
    }
    salvar_log(registro)

    imprimir_seguro("Mentor:", resposta_mentor)
    imprimir_seguro("LLM   :", resposta_llm)
    print("✅ Registrado em", LOG.as_posix())


if __name__ == "__main__":
    main()
