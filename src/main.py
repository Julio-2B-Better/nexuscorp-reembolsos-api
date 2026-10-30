from fastapi import FastAPI
from database import engine, Base
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gestão de Reembolsos",
    description="Sistema de centralização de reembolsos da NexusCorp",
    version="1.0.0"
)

@app.get("/status")
def verificar_status():
    return {"status": "API operacional"}