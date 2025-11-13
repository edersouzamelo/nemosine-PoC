# -*- coding: utf-8 -*-
import os
import sys
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

# 🔧 Força UTF-8 mesmo no Windows + VSCode
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    # Compatibilidade para Python < 3.7
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 🔐 API Key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("Nemosine PoC (Desktop) ativo.")
print("Diga ao Mentor o que você quer agora:")

while True:
    try:
        user_input = input("> ")
        if user_input.lower().strip() in ["sair", "exit", "quit"]:
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
        print("\nMentor:", ''.join(c if ord(c) < 128 else '?' for c in output_text))



        # 🔒 Log com UTF-8
        log = {
            "timestamp": datetime.utcnow().isoformat(),
            "pergunta": user_input,
            "resposta": output_text
        }

        path = Path("data/outputs/logs.jsonl")
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(log, ensure_ascii=False) + "\n")
        print("✅ Registrado em data/outputs/logs.jsonl\n")

    except Exception as e:
        print("LLM  : (erro interno) —", str(e))
