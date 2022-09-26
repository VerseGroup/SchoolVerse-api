FROM python:3.9

WORKDIR /app

# RUN pip install --upgrade setuptools

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./run.sh /app/run.sh

RUN chmod +x /app/run.sh

COPY ./scripts /app/scripts

RUN chmod +x /app/scripts/*.sh

COPY ./logs /app/logs

COPY ./driver /app/driver

COPY ./secrets /app/secrets

COPY ./tests /app/tests

COPY ./lib /app/lib

COPY .env /app/.env

COPY ./src /app/src

CMD ["sh", "./run.sh"]