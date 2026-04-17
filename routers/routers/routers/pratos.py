from fastapi import APIRouter, HTTPException
from models.prato import PratoInput, PratoOutput, DisponibilidadeInput
from typing import Optional
from datetime import datetime

router = APIRouter()

pratos = [
    {"id": 1, "nome": "Margherita", "categoria": "pizza", "preco": 45.0, "preco_promocional": None, "descricao": "Clássica com molho de tomate e mussarela", "disponivel": True, "criado_em": "2024-01-01T00:00:00"},
    {"id": 2, "nome": "Carbonara", "categoria": "massa", "preco": 52.0, "preco_promocional": None, "descricao": "Espaguete com ovo, queijo pecorino e guanciale", "disponivel": True, "criado_em": "2024-01-01T00:00:00"},
    {"id": 3, "nome": "Lasanha Bolonhesa", "categoria": "massa", "preco": 58.0, "preco_promocional": 49.0, "descricao": "Lasanha com ragù de carne e bechamel", "disponivel": False, "criado_em": "2024-01-01T00:00:00"},
    {"id": 4, "nome": "Tiramisù", "categoria": "sobremesa", "preco": 28.0, "preco_promocional": None, "descricao": "Clássica sobremesa italiana com mascarpone", "disponivel": True, "criado_em": "2024-01-01T00:00:00"},
    {"id": 5, "nome": "Quattro Stagioni", "categoria": "pizza", "preco": 49.0, "preco_promocional": None, "descricao": "Pizza com quatro recheios distintos por fatia", "disponivel": True, "criado_em": "2024-01-01T00:00:00"},
    {"id": 6, "nome": "Panna Cotta", "categoria": "sobremesa", "preco": 24.0, "preco_promocional": None, "descricao": "Creme cozido com calda de frutas vermelhas", "disponivel": True, "criado_em": "2024-01-01T00:00:00"},
]


@router.get("/", response_model=list[PratoOutput])
async def listar_pratos(
    categoria: Optional[str] = None,
    preco_maximo: Optional[float] = None,
    apenas_disponiveis: bool = False,
):
    resultado = pratos
    if categoria:
        resultado = [p for p in resultado if p["categoria"] == categoria]
    if preco_maximo:
        resultado = [p for p in resultado if p["preco"] <= preco_maximo]
    if apenas_disponiveis:
        resultado = [p for p in resultado if p["disponivel"]]
    return resultado


@router.get("/{prato_id}", response_model=PratoOutput)
async def buscar_prato(prato_id: int, formato: str = "completo"):
    for prato in pratos:
        if prato["id"] == prato_id:
            if formato == "resumido":
                return {**prato, "nome": prato["nome"], "preco": prato["preco"]}
            return prato
    raise HTTPException(status_code=404, detail=f"Prato com id {prato_id} não encontrado")


@router.post("/", response_model=PratoOutput, status_code=201)
async def criar_prato(prato: PratoInput):
    novo_id = max(p["id"] for p in pratos) + 1
    novo_prato = {
        "id": novo_id,
        "criado_em": datetime.now().isoformat(),
        **prato.model_dump(),
    }
    pratos.append(novo_prato)
    return novo_prato


@router.put("/{prato_id}/disponibilidade", response_model=PratoOutput)
async def alterar_disponibilidade(prato_id: int, body: DisponibilidadeInput):
    for prato in pratos:
        if prato["id"] == prato_id:
            prato["disponivel"] = body.disponivel
            return prato
    raise HTTPException(status_code=404, detail="Prato não encontrado")