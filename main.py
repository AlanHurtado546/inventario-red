from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Inventario de Red")


class Dispositivo(BaseModel):
    nombre: str
    tipo: str
    ip: str
    activo: bool = True


class DispositivoParcial(BaseModel):
    nombre: str | None = None
    tipo: str | None = None
    ip: str | None = None
    activo: bool | None = None


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
    return {"mensaje": "API de inventario funcionando"}


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


# POST - Alta
@app.post("/dispositivos", status_code=201)
def crear(nuevo: Dispositivo):

    if buscar(nuevo.nombre) is not None:
        raise HTTPException(
            status_code=409,
            detail=f"Ya existe el equipo {nuevo.nombre}"
        )

    inventario.append(nuevo)

    return nuevo


# PUT - Reemplazar dispositivo
@app.put("/dispositivos/{nombre}")
def reemplazar(nombre: str, datos: Dispositivo):

    equipo = buscar(nombre)

    if equipo is None:
        raise HTTPException(
            status_code=404,
            detail=f"No existe el equipo {nombre}"
        )

    inventario[inventario.index(equipo)] = datos

    return datos


# PATCH - Modificar algunos datos
@app.patch("/dispositivos/{nombre}")
def modificar(nombre: str, cambios: DispositivoParcial):

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