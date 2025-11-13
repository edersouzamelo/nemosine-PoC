import os
import json
import openai
import datetime
import sys
import io

# Corrige o encoding do terminal para UTF-8 no Windows
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

# Carrega a chave da API (ou substitua diretamente por sua chave)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Caminho do arquivo de log
log_path = "data/outputs/logs.jsonl"
os.makedirs(os.path.dirname(log_path), exist_ok=True)

# Função para gerar resposta da IA
def gerar_resposta(mensagem_usuario):
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é o Mentor do sistema Nemosine. Responda com clareza e foco em ação."},
                {"role": "user", "content": mensagem_usuario}
            ],
            temperature=0.7
        )
        return resposta.choices[0].message["content"].strip()

    except Exception as e:
        return f"(LLM erro) {str(e)}"

# Função para registrar no log
def registrar_log(mensagem_usuario, resposta_mentor):
    log = {
        "timestamp": datetime.datetime.now().isoformat(),
        "usuario": mensagem_usuario,
        "mentor": resposta_mentor
    }
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(log, ensure_ascii=False) + "\n")
    print("✅ Registrado em", log_path)

# Loop principal
def executar_menu():
    print("Nemosine PoC (Desktop) ativo.")
    while True:
        mensagem_usuario = input("Diga ao Mentor o que você quer agora:\n> ")
        if mensagem_usuario.lower() in ["sair", "exit", "quit"]:
            break
        resposta_mentor = gerar_resposta(mensagem_usuario)
        print("\nMentor:", resposta_mentor)
        registrar_log(mensagem_usuario, resposta_mentor)

if __name__ == "__main__":
    executar_menu()
