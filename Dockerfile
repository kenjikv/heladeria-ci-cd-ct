# Imagen del backend + frontend con el modelo ya entrenado
FROM python:3.12-slim

WORKDIR /app

# Primero las librerías (Docker reutiliza esta capa si no cambian)
COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

# Después el código, el modelo y la página web
COPY src/app.py src/app.py
COPY modelo/ modelo/
COPY frontend/ frontend/

EXPOSE 8000
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
