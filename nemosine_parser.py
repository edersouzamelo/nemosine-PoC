#!/usr/bin/env python3
# nemosine_parser.py

import json, csv, os

personas = {
    "Estratégicas": ["Mentor","Cientista","Filósofo","Mestre","Estrategista","Orquestrador","Vidente","Astrônomo","Burguês","Sócio","Engenheiro","Cigana","Guru","Louco"],
    "Simbólicas": ["Curador","Artista","Narrador","Vazio","Mentorzinho","Custódio","Espião","Bruxo","Arqueólogo","Exorcista","Promotor","Advogado","Juiz","Fantasma"],
    "Operacionais": ["Vigia","Executor","Mordomo","Treinador","Aprovisionador","Instrutor","Médico","Guardião","Bruto","Arauto","Adjunto","Comandante","Inimigo","Coveiro"],
    "Emocionais": ["Psicólogo","Terapeuta","Confessor","Espelho","Sombra","Dor","Desejo","Vingador","Fúria","Luz","Herdeiro","Princesa","Autor","Bobo_da_Corte"]
}

flat = []
idx = 1
for categoria, lista in personas.items():
    for nome in lista:
        flat.append({
            "id": idx,
            "nome": nome,
            "categoria": categoria,
            "descricao_curta": ""
        })
        idx += 1

outdir = "nemosine_output"
os.makedirs(outdir, exist_ok=True)

# salva JSON
with open(os.path.join(outdir, "personas.json"), "w", encoding="utf-8") as f:
    json.dump(flat, f, ensure_ascii=False, indent=2)

# salva CSV
with open(os.path.join(outdir, "personas.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id","nome","categoria","descricao_curta"])
    writer.writeheader()
    writer.writerows(flat)

print(f"Exportadas {len(flat)} personas com sucesso.")
print("Arquivos salvos em ./nemosine_output/")

