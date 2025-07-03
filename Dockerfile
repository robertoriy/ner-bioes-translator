FROM python:3.12-slim

WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --resume-retries 5 --no-cache-dir -r requirements.txt
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]