FROM python:3.11-slim

# Crear carpeta de trabajo
WORKDIR /app

# Copiar requirements.txt e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar scripts y archivos relevantes
COPY scripts/ scripts/
COPY *.csv ./

# Comando por defecto
CMD ["bash"]
