"""Pruebas del backend."""
from fastapi.testclient import TestClient

from app import app

cliente = TestClient(app)


def test_sirve_el_frontend():
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200
    assert "Heladería" in respuesta.text


def test_predice_mas_helados_con_mas_calor():
    frio = cliente.get("/api/predecir", params={"temperatura": 15}).json()["ventas"]
    calor = cliente.get("/api/predecir", params={"temperatura": 30}).json()["ventas"]
    assert 0 <= frio < calor


def test_rechaza_temperaturas_imposibles():
    assert cliente.get("/api/predecir", params={"temperatura": 90}).status_code == 422


def test_informa_el_modelo_desplegado():
    modelo = cliente.get("/api/modelo").json()
    assert {"pendiente", "intercepto", "mae", "entrenado"} <= modelo.keys()
