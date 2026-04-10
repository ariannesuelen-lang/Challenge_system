from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import auth, cursos, disciplinas, desafios, respostas, votos, admin

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(cursos.router)
app.include_router(disciplinas.router)
app.include_router(desafios.router)
app.include_router(respostas.router)
app.include_router(votos.router)
app.include_router(admin.router)