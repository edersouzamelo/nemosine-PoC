#!/usr/bin/env python3
# menu_nemosine.py — Navegação interativa das personas no terminal

import json, os

BASE = "nemosine_output/personas.json"

def carregar():
    if not os.path.exists(BASE):
        print("Arquivo não encontrado:", BASE)
        raise SystemExit(1)
    with open(BASE, encoding="utf-8") as f:
        return json.load(f)

def salvar(data):
    with open(BASE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def categorias(data):
    mapa = {}
    for p in data:
        mapa.setdefault(p["categoria"], []).append(p)
    return mapa

def listar_categorias(data):
    mapa = categorias(data)
    print("\nCategorias:")
    for i, (cat, itens) in enumerate(sorted(mapa.items()), 1):
        print(f" {i}. {cat} ({len(itens)})")
    print()

def listar_por_categoria(data):
    mapa = categorias(data)
    cats = list(sorted(mapa.keys()))
    for i, c in enumerate(cats, 1):
        print(f" {i}. {c} ({len(mapa[c])})")
    esc = input("\nEscolha o número da categoria: ").strip()
    if not esc.isdigit() or not (1 <= int(esc) <= len(cats)):
        print("Entrada inválida.\n")
        return
    cat = cats[int(esc)-1]
    print(f"\n— {cat} —")
    for p in mapa[cat]:
        print(f"  [{p['id']:02d}] {p['nome']}")
    print()

def buscar_por_nome(data):
    nome = input("\nNome da persona: ").strip()
    achou = None
    for p in data:
        if p["nome"].lower() == nome.lower():
            achou = p; break
    if not achou:
        print(f"Persona '{nome}' não encontrada.\n"); return
    print(f"\nID: {achou['id']}")
    print(f"Nome: {achou['nome']}")
    print(f"Categoria: {achou['categoria']}")
    print(f"Descrição: {achou['descricao_curta'] or '(vazia)'}\n")

def editar_descricao(data):
    nome = input("\nPersona para editar: ").strip()
    alvo = None
    for p in data:
        if p["nome"].lower() == nome.lower():
            alvo = p; break
    if not alvo:
        print(f"Persona '{nome}' não encontrada.\n"); return
    print(f"Descrição atual: {alvo['descricao_curta'] or '(vazia)'}")
    nova = input("Nova descrição curta (vazio mantém): ").strip()
    if nova:
        alvo["descricao_curta"] = nova
        salvar(data)
        print("Descrição atualizada.\n")
    else:
        print("Nada alterado.\n")

def listar_todas(data):
    print("\nTodas as personas:")
    for p in data:
        print(f" [{p['id']:02d}] {p['nome']} — {p['categoria']}")
    print()

def main():
    data = carregar()
    while True:
        print("=== Nemosine • Menu Interativo ===")
        print("1) Listar categorias")
        print("2) Listar personas por categoria")
        print("3) Buscar por nome")
        print("4) Editar descrição curta")
        print("5) Listar todas")
        print("0) Sair")
        op = input("> ").strip()
        if op == "1": listar_categorias(data)
        elif op == "2": listar_por_categoria(data)
        elif op == "3": buscar_por_nome(data)
        elif op == "4": editar_descricao(data); data = carregar()
        elif op == "5": listar_todas(data)
        elif op == "0": print("Fechando."); break
        else: print("Opção inválida.\n")

if __name__ == "__main__":
    main()
