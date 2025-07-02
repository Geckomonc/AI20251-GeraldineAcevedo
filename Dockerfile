FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Corrige estas líneas:
COPY apirest.py .
COPY client.py .
COPY train_data.csv .
COPY model.pkl .
COPY train.py .

EXPOSE 5001

CMD ["python", "apirest.py"]


