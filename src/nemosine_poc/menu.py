import sys
import os
import json

# 🔧 Forçar saída padrão para UTF-8 — compatível com PowerShell e terminal do VSCode
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')

def escrever_log(texto):
    try:
        with open("data/outputs/logs.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps({"mensagem": texto}, ensure_ascii=False) + "\n")
        print("✅ Registrado em data/outputs/logs.jsonl")
    except Exception as e:
        print(f"Erro ao escrever o log: {e}")

def mentor_responde(pergunta):
    # Simulação de resposta
    resposta = "Mentor: Sugestão: escreva o que você quer que o Nemosine faça agora em uma frase clara."
    return resposta

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
