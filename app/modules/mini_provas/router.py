import os, io, base64, qrcode
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Query
from .service import MiniProvaService
from .models import CorrecaoRequest
from uuid import UUID

load_dotenv()

# Carrega a URL do Frontend do .env (com fallback para localhost)
FRONTEND_URL = os.getenv("FRONTEND_URL")

router = APIRouter(prefix="/mini-provas", tags=["Mini-Provas"])
def get_mini_prova_service(): return MiniProvaService()

@router.get("/{prova_id}/iniciar/{usuario_id}")
def iniciar_prova(prova_id: UUID, usuario_id: int, service: MiniProvaService = Depends(get_mini_prova_service)):
    return service.iniciar_prova(prova_id, usuario_id)

@router.post("/corrigir")
def corrigir_prova(correcao: CorrecaoRequest, service: MiniProvaService = Depends(get_mini_prova_service)):
    return service.corrigir_prova(correcao)

@router.get("/mini-provas/{prova_id}/qrcode")
def gerar_qrcode_link_acesso(prova_id: UUID, aluno_id: UUID = Query(None)):
    """
    Gera um link compartilhável e um QR Code em Base64 para acesso à prova.
    Se o aluno_id for fornecido, o link já deixa o aluno logado na prova (modo quiosque).
    Se não, o link leva para a tela de login/identificação da prova.
    """
    try:
        # 1. Valida se a prova existe e está liberada para evitar geração de códigos para rascunhos
        res_prova = supabase.table("mini_provas").select("status, titulo").eq("id", str(prova_id)).single().execute()
        
        if not res_prova.data:
            raise HTTPException(status_code=404, detail="Mini-prova não encontrada.")
            
        prova = res_prova.data
        if prova["status"] != "liberada":
            raise HTTPException(status_code=400, detail=f"Não é possível gerar acesso. Status atual: {prova['status']}")

        # 2. Monta a URL de acesso dinamicamente
        if aluno_id:
            # Link direto (ex: para tablets em sala de aula onde o aluno já está identificado)
            url_acesso = f"{FRONTEND_URL}/prova/{prova_id}/aluno/{aluno_id}"
        else:
            # Link genérico (ex: projetor na sala, o aluno acessa e digita sua matrícula/turma)
            url_acesso = f"{FRONTEND_URL}/prova/{prova_id}"

        # 3. Gera o QR Code usando a biblioteca qrcode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url_acesso)
        qr.make(fit=True)

        # Cria a imagem (Pillow)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # 4. Converte a imagem para Base64 para trafegar via JSON
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        # Adiciona o cabeçalho de dados para o HTML reconhecer como imagem automaticamente
        img_data_uri = f"data:image/png;base64,{img_base64}"

        return {
            "mensagem": "QR Code gerado com sucesso.",
            "prova_titulo": prova["titulo"],
            "url_acesso": url_acesso,
            "qrcode_base64": img_data_uri
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar QR Code: {str(e)}")