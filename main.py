from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Inventario de Red")


# Modelo principal
class Dispositivo(BaseModel):
    nombre: str
    tipo: str
    ip: str
    activo: bool = True


# Modelo para PATCH
class DispositivoParcial(BaseModel):
    nombre: str | None = None
    tipo: str | None = None
    ip: str | None = None
    activo: bool | None = None


# Inventario inicial
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


# Busca un dispositivo por nombre
def buscar(nombre: str) -> Dispositivo | None:

    for equipo in inventario:

        if equipo.nombre.upper() == nombre.upper():
            return equipo

    return None


# Ruta principal
@app.get("/")
def inicio():

    return {
        "mensaje": "API de inventario funcionando"
    }


# GET - Mostrar todos
@app.get("/dispositivos")
def listar():

    return inventario


# GET - Buscar uno
@app.get("/dispositivos/{nombre}")
def obtener(nombre: str):

    equipo = buscar(nombre)

    if equipo is None:

        raise HTTPException(
            status_code=404,
            detail=f"No existe el equipo {nombre}"
        )

    return equipo


# PUT - Reemplazar completamente un dispositivo
@app.put("/dispositivos/{nombre}")
async def reemplazar(nombre: str, datos: Dispositivo):

    equipo = buscar(nombre)

    if equipo is None:

        raise HTTPException(
            status_code=404,
            detail=f"No existe el equipo {nombre}"
        )

    inventario[inventario.index(equipo)] = datos

    return datos


# PATCH - Modificar solo algunos datos
@app.patch("/dispositivos/{nombre}")
async def modificar(nombre: str, cambios: DispositivoParcial):

    equipo = buscar(nombre)

    if equipo is None:

        raise HTTPException(
            status_code=404,
            detail=f"No existe el equipo {nombre}"
        )

    for campo, valor in cambios.model_dump(
        exclude_unset=True
    ).items():

        setattr(equipo, campo, valor)

    return equipo