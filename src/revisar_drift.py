"""Compara los datos nuevos con los de entrenamiento y decide si hay que reentrenar.

Uso: python src/revisar_drift.py <datos_nuevos.csv>
- Data drift: cambió la temperatura que llega (prueba de Kolmogórov-Smirnov).
- Concept drift: con los datos nuevos el modelo ya no pasa la puerta de calidad.
Solo el concept drift obliga a reentrenar; el data drift se vigila.
"""
import json
import os
import sys

import pandas as pd
from scipy.stats import ks_2samp

from entrenar import MAE_MAXIMO


def revisar(viejos, nuevos, modelo):
    """Devuelve el resultado de las dos revisiones."""
    p_valor = ks_2samp(viejos["temperatura"], nuevos["temperatura"]).pvalue   # ¿misma distribución?
    prediccion = modelo["pendiente"] * nuevos["temperatura"] + modelo["intercepto"]
    error = (nuevos["ventas"] - prediccion).abs().mean()                     # MAE con los datos nuevos
    return {
        "p_valor": float(p_valor),
        "data_drift": bool(p_valor < 0.05),             # p < 0.05: las temperaturas cambiaron
        "error": round(float(error), 2),
        "concept_drift": bool(error > MAE_MAXIMO),      # se equivoca más de lo aceptado
    }


if __name__ == "__main__":
    archivo = sys.argv[1] if len(sys.argv) > 1 else "datos/nuevos.csv"
    viejos = pd.read_csv("datos/ventas.csv")               # datos con los que se entrenó el modelo actual
    nuevos = pd.read_csv(archivo)
    with open("modelo/modelo.json") as f:
        modelo = json.load(f)

    r = revisar(viejos, nuevos, modelo)
    reentrenar = r["concept_drift"]
    informe = [
        "| Revisión | Resultado |",
        "|---|---|",
        f"| Data drift (p-valor KS = {r['p_valor']:.3g}) | {'sí' if r['data_drift'] else 'no'} |",
        f"| Error con datos nuevos (antes {modelo['mae']}) | {r['error']} |",
        f"| Concept drift (error > {MAE_MAXIMO}) | {'sí' if r['concept_drift'] else 'no'} |",
        f"| **Decisión** | **{'REENTRENAR' if reentrenar else 'el modelo sigue sirviendo'}** |",
    ]
    print("\n".join(informe))

    # GitHub Actions: la salida 'reentrenar' la leen los pasos siguientes
    # y el informe aparece en el resumen de la ejecución.
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"reentrenar={'true' if reentrenar else 'false'}\n")
    if "GITHUB_STEP_SUMMARY" in os.environ:
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
            f.write("## Revisión de drift\n\n" + "\n".join(informe) + "\n")
