FROM python:3.13-slim

WORKDIR /app

COPY ./src /app

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update
RUN apt-get install -y supervisor
COPY ./tools/supervisord.conf /etc/supervisor/supervisord.conf

EXPOSE 8000

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]