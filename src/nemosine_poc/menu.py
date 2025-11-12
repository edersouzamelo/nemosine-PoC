# Nemosine PoC – Mentor respondendo (v0.4-min, com cliente LLM simulado)
from pathlib import Path
import json
from nemosine_poc.llm_client import enviar_para_llm   # [NOVA 1]

OUT = Path("data/outputs"); OUT.mkdir(parents=True, exist_ok=True)
LOG = OUT / "logs.jsonl"

def mentor_responde(pedido: str) -> str:
    t = pedido.lower()
    if "passo" in t or "hoje" in t or "agora" in t:
        return "Passo único de hoje: atualizar o README com a frase 'PoC ativo no desktop' e fazer commit."
    if "readme" in t:
        return "Abra README.md, adicione 'PoC ativo no desktop (branch poc-desktop)' e faça commit curto."
    if "api" in t:
        return "Próximo: criar llm_client real com ChatGPT (colocar chave via .env)."
    if "repo" in t or "github" in t:
        return "Abra uma Issue 'PoC v0.3 – Mentor responde' e marque como done quando este script rodar."
    return "Sugestão: escolha 1 micro-ação que caiba em 5 minutos e me diga qual será."

print("Nemosine PoC (Desktop) ativo.")
pedido = input("Diga ao Mentor o que você quer agora:\n> ").strip() or "quero um passo concreto pra hoje"
mensagem = mentor_responde(pedido)

eco_llm = enviar_para_llm(pedido)         # [NOVA 2]

registro = {
    "persona": "Mentor",
    "lugar_do_atlas": "Núcleo",
    "mensagem": mensagem,
    "rastro": {"fonte": "Mentor", "coerencia": 0.9, "referencias": []},
    "pedido": pedido,
    "llm_echo": eco_llm                    # [NOVA 3]
}

with LOG.open("a", encoding="utf-8") as f:
    f.write(json.dumps(registro, ensure_ascii=False) + "\n")

print("Mentor:", mensagem)
print(eco_llm)  # mostra o retorno do cliente (simulado por enquanto)
print("✅ Registrado em data/outputs/logs.jsonl")
