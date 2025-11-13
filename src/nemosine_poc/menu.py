import os
from openai import OpenAI
from dotenv import load_dotenv
import json
from datetime import datetime

# Carrega a chave da API do .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Mensagem inicial do sistema
print("Nemosine PoC (Desktop) ativo.")
print("Diga ao Mentor o que você quer agora:")

# Loop principal
while True:
    try:
        user_input = input("> ")
        if user_input.strip().lower() in ["sair", "exit", "quit"]:
            print("Encerrando Nemosine.")
            break

        # Envia para o modelo
        resposta = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é o Mentor do sistema Nemosine."},
                {"role": "user", "content": user_input}
            ]
        )

        output_text = resposta.choices[0].message.content.strip()
        print("\nMentor:", output_text)

        # Salva o log da interação
        log = {
            "timestamp": datetime.utcnow().isoformat(),
            "pergunta": user_input,
            "resposta": output_text
        }

        os.makedirs("data/outputs", exist_ok=True)
        with open("data/outputs/logs.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(log, ensure_ascii=False) + "\n")
        print("✅ Registrado em data/outputs/logs.jsonl")

    except Exception:
        # Silencia erro de print com encoding (ex: '\u2014' em terminal que não aceita UTF-8)
        print("\nLLM  : (erro interno não exibido no console)")
