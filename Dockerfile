FROM python:3.9-alpine

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./run.sh /app/run.sh

RUN chmod +x /app/run.sh

COPY ./scripts /app/scripts

RUN chmod +x /app/scripts/*

RUN sh /app/scripts/InstallChrome.sh

COPY ./logs /app/logs

COPY ./driver /app/driver

COPY ./src /app/src

CMD ["sh", "./run.sh"]