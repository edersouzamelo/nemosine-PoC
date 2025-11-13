# -*- coding: utf-8 -*-

import sys
import io
import json
from pathlib import Path
import openai

# ============================================================
# 1. FORÇA O TERMINAL/VS CODE/POWERSHELL A USAR UTF‑8 DE VERDADE
# ============================================================
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ============================================================
# 2. COLOQUE SUA CHAVE AQUI — EXATAMENTE AQUI
# ============================================================
openai.api_key = "COLOQUE_SUA_API_KEY_AQUI"

# ============================================================
# 3. PASTA DE SAÍDA (logs)
# ============================================================
OUT = Path("data/outputs")
OUT.mkdir(parents=True, exist_ok=True)

# ============================================================
# 4. LOOP PRINCIPAL
# ============================================================
print("Nemosine PoC (Desktop) ativo.")
print("Diga ao Mentor o que você quer agora:")

while True:
    pergunta = input("> ").strip()

    if not pergunta:
        continue

    # ============================================================
    # 5. CHAMADA REAL À OPENAI
    # ============================================================
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é o Mentor do Sistema Nemosine."},
                {"role": "user", "content": pergunta}
            ]
        )

        texto = resposta.choices[0].message["content"]

    except Exception as e:
        print("\n[ERRO LLM] →", str(e))
        texto = "Erro do modelo."

    # ============================================================
    # 6. MOSTRA NO TERMINAL (UTF‑8 GARANTIDO)
    # ============================================================
    print("\nMentor:", texto)

    # ============================================================
    # 7. SALVA EM JSON (UTF‑8 GARANTIDO)
    # ============================================================
    registro = {
        "pergunta": pergunta,
        "resposta": texto
    }

    with open(OUT / "logs.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")

    print("✔ Registrado em data/outputs/logs.jsonl\n")
    print("Diga ao Mentor o que você quer agora:")
