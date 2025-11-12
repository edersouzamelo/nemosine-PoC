from pathlib import Path
import json

OUT = Path("data/outputs")
OUT.mkdir(parents=True, exist_ok=True)

print("Nemosine PoC (Desktop) — diga algo para registrar:")
texto = input("> ").strip() or "teste padrão"

registro = {
    "persona": "Mentor",
    "lugar_do_atlas": "Núcleo",
    "mensagem": f"O usuário disse: {texto}",
    "rastro": {"fonte": "Mentor", "coerencia": 0.9, "referencias": []}
}

(OUT / "logs.jsonl").open("a", encoding="utf-8").write(json.dumps(registro, ensure_ascii=False) + "\n")
print("Registrado em data/outputs/logs.jsonl ✅")

