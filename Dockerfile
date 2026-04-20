FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8081
EXPOSE 8501

RUN chmod 755 ./scripts/entrypoint.sh
CMD ["./scripts/entrypoint.sh"]