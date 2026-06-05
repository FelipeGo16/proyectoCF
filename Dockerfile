# 1. Imagen base ligera de Python
FROM python:3.9-slim

# 2. Evita que Python genere archivos .pyc y permite ver logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 5. Copiamos e instalamos dependencias de Python primero (Caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiamos el resto del código de la aplicación
COPY . .

# 7. Exponemos el puerto que usará Flask/Gunicorn
EXPOSE 5000

# 8. Comando para ejecutar con Gunicorn (Producción)
# -w 4: Cuatro procesos trabajadores para manejar tráfico en paralelo
# -b: Dirección y puerto donde escuchará
# app:app -> Nombre del archivo (app.py) : Nombre de la variable Flask (app)
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "app:app"]

