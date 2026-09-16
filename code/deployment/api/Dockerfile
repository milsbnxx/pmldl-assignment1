FROM python:3.11-slim

WORKDIR /app

COPY code/deployment/api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY code/deployment/api/main.py /app/main.py
COPY models/model.joblib /app/models/model.joblib

ENV MODEL_PATH=/app/models/model.joblib

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
