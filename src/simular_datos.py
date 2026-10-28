"""Simula los datos nuevos que llegan a la heladería.

En la vida real vendrían de la caja registradora o de una base de datos.
Uso: python src/simular_datos.py <escenario> <archivo_de_salida>
"""
import sys

import numpy as np
import pandas as pd

# Cada escenario es una "semana" distinta en la heladería:
# temperatura media y la regla real que une temperatura con ventas.
ESCENARIOS = {
    "normal": {"temperatura": 20, "pendiente": 8, "intercepto": -60},       # primavera, precio normal
    "verano": {"temperatura": 30, "pendiente": 8, "intercepto": -60},       # más calor, misma regla -> data drift
    "precio_alto": {"temperatura": 30, "pendiente": 5, "intercepto": -40},  # con el mismo calor se vende menos -> concept drift
    "datos_malos": {"temperatura": 20, "pendiente": 8, "intercepto": -60},  # como normal, pero con errores de carga
}


def simular(escenario, dias=100, semilla=None):
    """Devuelve una tabla con la temperatura y las ventas de cada día."""
    regla = ESCENARIOS[escenario]                                    # la regla del escenario elegido
    rng = np.random.default_rng(semilla)                             # generador de números aleatorios
    temperatura = rng.normal(regla["temperatura"], 3, dias).round(1)  # temperatura de cada día (°C)
    ruido = rng.normal(0, 10, dias)                                  # lo que el modelo no puede explicar
    ventas = regla["pendiente"] * temperatura + regla["intercepto"] + ruido
    ventas = np.clip(ventas, 0, None).round().astype(int)            # no se venden helados negativos
    datos = pd.DataFrame({"temperatura": temperatura, "ventas": ventas})

    if escenario == "datos_malos":
        datos.loc[:4, "temperatura"] = None   # un sensor roto: celdas vacías
        datos.loc[5:9, "ventas"] = -1         # un error al cargar: ventas negativas
    return datos


if __name__ == "__main__":
    escenario = sys.argv[1] if len(sys.argv) > 1 else "normal"
    archivo = sys.argv[2] if len(sys.argv) > 2 else "datos/nuevos.csv"
    simular(escenario).to_csv(archivo, index=False)
    print(f"Escenario '{escenario}': 100 días nuevos guardados en {archivo}")
