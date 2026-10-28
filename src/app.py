"""Backend: sirve el frontend y responde predicciones con el modelo guardado.

Uso: uvicorn src.app:app --reload
"""
import json
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse

RAIZ = Path(__file__).resolve().parent.parent                       # carpeta del proyecto
MODELO = json.loads((RAIZ / "modelo" / "modelo.json").read_text())  # se lee una vez al arrancar

app = FastAPI(title="Heladería")


@app.get("/")
def frontend():
    """La página web."""
    return FileResponse(RAIZ / "frontend" / "index.html")


@app.get("/api/modelo")
def modelo():
    """Los datos del modelo desplegado: la recta, su error y cuándo se entrenó."""
    return MODELO


@app.get("/api/predecir")
def predecir(temperatura: float = Query(ge=-10, le=50)):
    """Cuántos helados se venderán con esa temperatura."""
    ventas = MODELO["pendiente"] * temperatura + MODELO["intercepto"]
    return {"temperatura": temperatura, "ventas": max(0, round(ventas))}
