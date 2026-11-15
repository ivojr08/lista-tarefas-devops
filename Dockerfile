FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN useradd --create-home appuser && mkdir -p /app/data && chown appuser:appuser /app/data
COPY app ./app
ARG APP_VERSION=local
ENV APP_VERSION=$APP_VERSION PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
USER appuser
EXPOSE 8000
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
