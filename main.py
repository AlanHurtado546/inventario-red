from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Dispositivo(BaseModel):
    id: Optional[int] = None
    nombre: str
    tipo: str
    ip: str
    ubicacion: str

dispositivos = []

@app.post("/dispositivos/", status_code=201)
def agregar_dispositivo(dispositivo: Dispositivo):
    dispositivo.id = len(dispositivos) + 1
    dispositivos.append(dispositivo)
    return {
        "mensaje": "Dispositivo agregado correctamente",
        "dispositivo": dispositivo
    }

