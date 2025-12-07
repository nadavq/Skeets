FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY language_service/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY language_service/ ./language_service
COPY shared/ ./shared

CMD ["uvicorn", "language_service.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]