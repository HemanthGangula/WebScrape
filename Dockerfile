FROM node:18-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y chromium libxss1 libnss3 libatk-bridge2.0-0 libgtk-3-0 libgbm1 \
    python3 python3-pip python3-venv

COPY . .

RUN chmod +x /app/entrypoint.sh

WORKDIR /app/scraper
RUN npm install

WORKDIR /app
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
ENV VIRTUAL_ENV="/app/venv"

RUN pip3 install --no-cache-dir flask

ENV PYTHONUNBUFFERED=1

CMD ["/app/entrypoint.sh"]

