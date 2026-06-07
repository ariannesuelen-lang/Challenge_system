from fastapi import APIRouter, Depends
from .service import UsuarioService
from .models import UsuarioCreate, UsuarioResponse
from typing import List

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

def get_usuario_service():
    return UsuarioService()

@router.post("/", response_model=UsuarioResponse)
def criar_usuario(usuario: UsuarioCreate, service: UsuarioService = Depends(get_usuario_service)):
    return service.cadastrar(usuario)

@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(service: UsuarioService = Depends(get_usuario_service)):
    return service.listar()