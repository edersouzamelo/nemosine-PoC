#!/usr/bin/env python3
# get_persona.py

import json, sys

with open("nemosine_output/personas.json", encoding="utf-8") as f:
    data = json.load(f)

def get_persona(nome):
    for p in data:
        if p["nome"].lower() == nome.lower():
            return p
    return None

if len(sys.argv) < 2:
    print("Uso: python get_persona.py <NomeDaPersona>")
    sys.exit()

nome = " ".join(sys.argv[1:])
p = get_persona(nome)
if p:
    print(f"\nID: {p['id']}")
    print(f"Nome: {p['nome']}")
    print(f"Categoria: {p['categoria']}")
    print(f"Descrição: {p['descricao_curta'] or '(vazia)'}\n")
else:
    print(f"Persona '{nome}' não encontrada.")
