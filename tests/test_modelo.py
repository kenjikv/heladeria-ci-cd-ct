"""Pruebas del entrenamiento, del modelo guardado y de la revisión de drift."""
import json

import pandas as pd

from entrenar import MAE_MAXIMO, entrenar
from revisar_drift import revisar
from simular_datos import simular


def test_aprende_la_regla_del_mundo():
    modelo = entrenar(simular("normal", semilla=1))
    assert 6 < modelo["pendiente"] < 10        # la regla real es 8 helados por grado
    assert modelo["mae"] < MAE_MAXIMO


def test_el_modelo_del_repositorio_pasa_la_puerta_de_calidad():
    with open("modelo/modelo.json") as f:
        modelo = json.load(f)
    datos = pd.read_csv("datos/ventas.csv")
    error = (datos["ventas"] - (modelo["pendiente"] * datos["temperatura"] + modelo["intercepto"])).abs().mean()
    assert error < MAE_MAXIMO


def test_detecta_data_drift_sin_concept_drift():
    viejos = simular("normal", semilla=1)
    modelo = entrenar(viejos)
    r = revisar(viejos, simular("verano", semilla=2), modelo)
    assert r["data_drift"] and not r["concept_drift"]


def test_detecta_concept_drift():
    viejos = simular("verano", semilla=1)
    modelo = entrenar(viejos)
    r = revisar(viejos, simular("precio_alto", semilla=2), modelo)
    assert r["concept_drift"]
