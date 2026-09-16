FROM python:3.11-slim

WORKDIR /app

COPY code/deployment/app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY code/deployment/app/app.py /app/app.py

ENV API_URL=http://api:8000

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
