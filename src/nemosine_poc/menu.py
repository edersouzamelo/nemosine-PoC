# Nemosine PoC – Porta de Entrada (Desktop) v0.2-min
from pathlib import Path
import json

OUT = Path("data/outputs")
OUT.mkdir(parents=True, exist_ok=True)
LOG = OUT / "logs.jsonl"

print("Nemosine PoC (Desktop) ativo.")
texto = input("Diga ao Mentor o que você quer agora:\n> ").strip() or "explica como retomar hoje"

registro = {
    "persona": "Mentor",
    "lugar_do_atlas": "Núcleo",
    "mensagem": f"Recebi: {texto}. Próximo passo: escolher a ação concreta de hoje.",
    "rastro": {"fonte": "Mentor", "coerencia": 0.9, "referencias": []}
}

with LOG.open("a", encoding="utf-8") as f:
    f.write(json.dumps(registro, ensure_ascii=False) + "\n")

print("✅ Registrado em data/outputs/logs.jsonl")
