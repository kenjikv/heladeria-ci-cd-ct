"""Pruebas de la validación de datos."""
import pandas as pd

from simular_datos import simular
from validar_datos import validar


def test_los_datos_del_repositorio_son_validos():
    assert validar(pd.read_csv("datos/ventas.csv")) == []


def test_datos_simulados_normales_son_validos():
    assert validar(simular("normal", semilla=1)) == []


def test_detecta_datos_malos():
    problemas = validar(simular("datos_malos", semilla=1))
    assert any("celdas vacías" in p for p in problemas)
    assert any("ventas negativas" in p for p in problemas)


def test_detecta_columnas_equivocadas():
    datos = pd.DataFrame({"temp": [20] * 50, "ventas": [100] * 50})
    assert "columnas" in validar(datos)[0]


def test_detecta_pocas_filas():
    assert "filas" in validar(simular("normal", dias=10, semilla=1))[0]
