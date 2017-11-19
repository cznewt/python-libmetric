FROM python:2.7-slim-jessie

RUN apt-get update && apt-get -y install librrd-dev libpython-dev
WORKDIR /code
ADD . .
RUN pip install .

ENTRYPOINT ["instant_alarm"]
