"""Verifica que un archivo de datos sirva para entrenar el modelo.

Uso: python src/validar_datos.py <archivo.csv>
Si encuentra problemas termina con código 1 y el pipeline se detiene.
"""
import sys

import pandas as pd

COLUMNAS = ["temperatura", "ventas"]   # columnas que esperamos, en este orden
MINIMO_FILAS = 30                      # con menos días no se puede entrenar bien


def validar(datos):
    """Devuelve la lista de problemas encontrados (vacía si todo está bien)."""
    if list(datos.columns) != COLUMNAS:
        return [f"las columnas deben ser {COLUMNAS} y son {list(datos.columns)}"]
    for columna in COLUMNAS:
        if not pd.api.types.is_numeric_dtype(datos[columna]):
            return [f"la columna '{columna}' tiene valores que no son números"]

    problemas = []
    if len(datos) < MINIMO_FILAS:
        problemas.append(f"hay {len(datos)} filas y se necesitan al menos {MINIMO_FILAS}")
    if datos.isna().any().any():
        problemas.append(f"hay {datos.isna().sum().sum()} celdas vacías")
    if not datos["temperatura"].dropna().between(-10, 50).all():
        problemas.append("hay temperaturas fuera del rango de -10 a 50 °C")
    if (datos["ventas"] < 0).any():
        problemas.append(f"hay {(datos['ventas'] < 0).sum()} días con ventas negativas")
    return problemas


if __name__ == "__main__":
    archivo = sys.argv[1] if len(sys.argv) > 1 else "datos/ventas.csv"
    problemas = validar(pd.read_csv(archivo))
    for problema in problemas:
        print(f"ERROR: {problema}")
    if problemas:
        sys.exit(1)   # código distinto de 0 = el paso falla en GitHub Actions
    print(f"OK: {archivo} pasó la validación")
