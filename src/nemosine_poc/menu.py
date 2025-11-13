# -*- coding: utf-8 -*-
import os
import sys
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

# Configura terminal para UTF-8
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Carrega a chave da API do .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Mensagem inicial
print("Nemosine PoC (Desktop) — diga algo ao Mentor:")

# Loop principal
while True:
    try:
        user_input = input("> ")
        if user_input.strip().lower() in ["sair", "exit", "quit"]:
            print("Encerrando Nemosine.")
            break

        resposta = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é o Mentor do sistema Nemosine."},
                {"role": "user", "content": user_input}
            ]
        )

        output_text = resposta.choices[0].message.content.strip()
        print("\nMentor:", output_text)

        # Salva no log
        log = {
            "timestamp": datetime.utcnow().isoformat(),
            "pergunta": user_input,
            "resposta": output_text
        }

        output_path = Path("data/outputs/logs.jsonl")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(log, ensure_ascii=False) + "\n")
        print("✅ Registrado em data/outputs/logs.jsonl")

    except Exception:
        print("\nLLM  : (erro interno não exibido no console)")
