FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8081
EXPOSE 8501

RUN adduser --disabled-password rondi && \
    usermod -aG sudo rondi && \
    echo "rondi ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers \
    chmod 755 ./scripts/entrypoint.sh && \
    chown -R rondi:rondi /app

USER rondi

CMD ["./scripts/entrypoint.sh"]