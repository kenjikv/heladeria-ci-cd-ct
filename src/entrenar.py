"""Entrena el modelo y lo guarda solo si es lo bastante bueno.

Uso: python src/entrenar.py <archivo.csv>
El modelo es una recta: ventas = pendiente * temperatura + intercepto.
Se guarda en modelo/modelo.json, un archivo de texto fácil de leer en git.
"""
import json
import sys
from datetime import datetime, timezone

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

MAE_MAXIMO = 15                       # puerta de calidad: error máximo aceptado (helados por día)
ARCHIVO_MODELO = "modelo/modelo.json"


def entrenar(datos):
    """Entrena con el 80 % de los días y mide el error con el 20 % restante."""
    X_entreno, X_prueba, y_entreno, y_prueba = train_test_split(
        datos[["temperatura"]], datos["ventas"], test_size=0.2, random_state=0
    )
    recta = LinearRegression().fit(X_entreno, y_entreno)                  # aprende la recta
    mae = mean_absolute_error(y_prueba, recta.predict(X_prueba))          # error con días que no vio
    return {
        "pendiente": round(float(recta.coef_[0]), 3),
        "intercepto": round(float(recta.intercept_), 3),
        "mae": round(float(mae), 2),
        "dias": len(datos),
        "entrenado": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    }


if __name__ == "__main__":
    archivo = sys.argv[1] if len(sys.argv) > 1 else "datos/ventas.csv"
    modelo = entrenar(pd.read_csv(archivo))
    signo = "-" if modelo["intercepto"] < 0 else "+"
    print(f"Modelo: ventas = {modelo['pendiente']} * temperatura {signo} {abs(modelo['intercepto'])}")
    print(f"Error medio (MAE): {modelo['mae']} helados por día")

    if modelo["mae"] > MAE_MAXIMO:
        print(f"ERROR: el MAE supera {MAE_MAXIMO}; el modelo no se guarda")
        sys.exit(1)

    with open(ARCHIVO_MODELO, "w") as f:
        json.dump(modelo, f, indent=2)
    print(f"OK: modelo guardado en {ARCHIVO_MODELO}")
