# Exemple de Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Utilisez la syntaxe de factory
CMD ["gunicorn", "app:create_app()", "--bind", "0.0.0.0:5000", "--workers", "4"]
