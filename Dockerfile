FROM python:3.9-alpine

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./run.sh /app/run.sh

RUN chmod +x /app/run.sh

COPY ./src /app/src

CMD ["sh", "./run.sh"]