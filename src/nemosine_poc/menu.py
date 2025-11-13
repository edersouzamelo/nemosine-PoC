#!/usr/bin/env python3
# Nemosine PoC – Mentor + LLM num arquivo só (versão HTTP cru, sem lib openai)

import sys
from pathlib import Path
import json
import os
import urllib.request
import urllib.error

from dotenv import load_dotenv


# -------------------------------------------------------------------
# Config de saída e paths
# -------------------------------------------------------------------

try:
    # Tenta forçar UTF-8; se não der, segue a vida
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

OUT = Path("data/outputs")
OUT.mkdir(parents=True, exist_ok=True)
LOG = OUT / "logs.jsonl"


# -------------------------------------------------------------------
# Chamada manual à API do ChatGPT (HTTP cru)
# -------------------------------------------------------------------

def enviar_para_llm(pedido: str) -> str:
    """
    Chama a API de chat da OpenAI via HTTP.
    Não usa a biblioteca openai (pra evitar o bug de ascii).
    """
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    # pode ajustar esse nome se quiser outro modelo
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        return "(LLM off) Falta OPENAI_API_KEY no .env na raiz do projeto."

    url = "https://api.openai.com/v1/chat/completions"

    payload = {
        "model": model,
        "messages": [
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
    }

    data_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            resp_bytes = resp.read()
        resp_json = json.loads(resp_bytes.decode("utf-8", errors="replace"))
        # navega na estrutura padrão do /chat/completions
        choices = resp_json.get("choices", [])
        if not choices:
            return f"(LLM erro) resposta sem choices: {resp_json}"

        msg = choices[0].get("message", {})
        content = msg.get("content", "")
        if not content:
            return f"(LLM erro) resposta sem content: {resp_json}"

        return content

    except urllib.error.HTTPError as e:
        # tenta ler corpo de erro
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            body = ""
        return f"(LLM erro HTTP {e.code}) {e.reason} {body}"
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
        return "A API está ligada neste arquivo via HTTP direto. Se algo falhar, o erro aparece na linha 'LLM :'."
    return "Sugestão: escreva o que você quer que o Nemosine faça agora em uma frase clara."


# -------------------------------------------------------------------
# Utilitários: log + impressão segura
# -------------------------------------------------------------------

def salvar_log(registro: dict) -> None:
    try:
        with LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(registro, ensure_ascii=False) + "\n")
    except Exception:
        # se der zica no log, não mata o programa
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

    main()
