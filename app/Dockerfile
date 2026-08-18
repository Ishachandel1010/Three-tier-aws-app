FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["sh", "-c", "python3 -c 'from app import init_db; init_db()' && gunicorn --bind 0.0.0.0:5000 --workers 3 app:app"]
