from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

app = FastAPI(title="Inventario de Red")


class Dispositivo(BaseModel):
    nombre: str
    tipo: str
    ip: str
    activo: bool = True


inventario = [
    Dispositivo(
        nombre="R1",
        tipo="router",
        ip="10.0.0.1",
        activo=True
    ),
    Dispositivo(
        nombre="SW1",
        tipo="switch",
        ip="10.0.0.2",
        activo=True
    )
]


def buscar(nombre: str) -> Dispositivo | None:
    for equipo in inventario:
        if equipo.nombre.upper() == nombre.upper():
            return equipo

    return None


@app.get("/")
def inicio():
    return {
        "mensaje": "API de inventario funcionando"
    }


@app.get("/dispositivos")
def listar():
    return inventario


@app.get("/dispositivos/{nombre}")
def obtener(nombre: str):

    equipo = buscar(nombre)

    if equipo is None:
        raise HTTPException(
            status_code=404,
            detail=f"No existe el equipo {nombre}"
        )

    return equipo

@app.delete("/dispositivos/{nombre}", status_code=204)
async def eliminar(nombre: str):

    equipo = buscar(nombre)

    if equipo is None:
        raise HTTPException(
            status_code=404,
            detail=f"No existe el equipo {nombre}"
        )

    inventario.remove(equipo)

    return Response(status_code=204)