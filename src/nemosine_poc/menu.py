# -*- coding: utf-8 -*-

import sys
import os
import json

# 🔒 Forçar UTF-8 na saída padrão, independentemente do terminal
sys.stdout.reconfigure(encoding='utf-8')

# 📁 Garantir pasta de saída
os.makedirs("data/outputs", exist_ok=True)

# ✍️ Função para salvar logs
def escrever_log(texto):
    try:
        with open("data/outputs/logs.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps({"mensagem": texto}, ensure_ascii=False) + "\n")
        print("✅ Registrado em data/outputs/logs.jsonl")
    except Exception as e:
        print(f"Erro ao escrever o log: {e}")

# 🤖 Resposta simulada do Mentor (substituir pela chamada real à OpenAI depois)
def mentor_responde(pergunta):
    resposta = "Mentor: Sugestão: escreva o que você quer que o Nemosine faça agora em uma frase clara."
    return resposta

# 🚀 Execução principal
if __name__ == "__main__":
    print("Nemosine PoC (Desktop) ativo.")
    while True:
        try:
            entrada = input("Diga ao Mentor o que você quer agora:\n> ")
            if entrada.strip().lower() in ["sair", "exit", "q"]:
                break
            resposta = mentor_responde(entrada)
            print(resposta)
            escrever_log(resposta)
        except Exception as e:
            print(f"LLM  : (LLM erro) {e}")

