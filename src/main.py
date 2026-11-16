from fastapi import FastAPI
from src.database import engine, Base

import src.models.usuario
import src.models.solicitacao

from src.routes import auth 
from src.routes import reembolsos_routes
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gestão de Reembolsos",
    description="Sistema de centralização de reembolsos da NexusCorp",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(reembolsos_routes.router)

@app.get("/status")
def verificar_status():
    return {"status": "API operacional"}

@app.get("/")
def root():
    return {"mensagem": "API de Reembolsos NexusCorp a funcionar!"}