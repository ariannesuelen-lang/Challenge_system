from fastapi import FastAPI
from modules.usuarios.router import router as usuarios_router
from modules.questoes.router import router as questoes_router
from modules.mini_provas.router import router as mini_provas_router
from modules.relatorios.router import router as relatorios_router
import uvicorn

app = FastAPI(
    title="API Mini-Provas",
    description="Sistema de Mini Provas para avaliação de alunos, com funcionalidades de cadastro de usuários, questões, correção automática e geração de relatórios.",
    version="3.0"
)

app.include_router(usuarios_router)
app.include_router(questoes_router)
app.include_router(mini_provas_router)
app.include_router(relatorios_router)

if __name__ == "__main__":
    uvicorn.run(app)