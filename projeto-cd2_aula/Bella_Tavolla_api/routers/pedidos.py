from fastapi import APIRouter, HTTPException
from models.pedido import PedidoInput, PedidoOutput
from routers.pratos import pratos
import httpx
import os

router = APIRouter()
pedidos = []

# Chamada real para o modelo do Hugging Face
async def obter_preco_preditivo(prato_id: int):
    # Substitua 'SeuUsuario/SeuModelo' pela URL que você copiou no Hugging Face
    hf_api_url = "https://huggingface.co/joaogabriel101735/precificacao-bella-tavola"
    hf_token = os.getenv("HF_TOKEN")

    # Se rodar local sem token, ele apenas ignora sem quebrar a API
    if not hf_token:
        return None 

    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {"inputs": {"prato_id": prato_id}}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(hf_api_url, headers=headers, json=payload, timeout=3.0)
            if response.status_code == 200:
                resultado = response.json()
                # Ajuste "preco_sugerido" para o nome do campo que o seu modelo realmente devolve
                return resultado[0].get("preco_sugerido") if isinstance(resultado, list) else resultado.get("preco_sugerido")
            return None
    except Exception:
        return None

@router.post("/", response_model=PedidoOutput, status_code=201)
async def criar_pedido(pedido: PedidoInput):
    prato = next((p for p in pratos if p["id"] == pedido.prato_id), None)
    
    if not prato:
        raise HTTPException(status_code=404, detail="Prato não encontrado")
    if not prato["disponivel"]:
        raise HTTPException(status_code=400, detail=f"O prato '{prato['nome']}' não está disponível")

    # Tenta buscar do modelo. Se o modelo falhar, usa o preço normal.
    preco_ia = await obter_preco_preditivo(pedido.prato_id)
    preco_efetivo = preco_ia or prato["preco_promocional"] or prato["preco"]

    novo_pedido = {
        "id": len(pedidos) + 1,
        "prato_id": pedido.prato_id,
        "nome_prato": prato["nome"],
        "quantidade": pedido.quantidade,
        "valor_total": preco_efetivo * pedido.quantidade,
        "observacao": pedido.observacao,
    }
    pedidos.append(novo_pedido)
    return novo_pedido

@router.get("/", response_model=list[PedidoOutput])
async def listar_pedidos():
    return pedidos