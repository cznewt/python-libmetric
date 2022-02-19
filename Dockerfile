FROM python:3.9

RUN apt-get update && apt-get -y install librrd-dev libpython-dev
WORKDIR /code
ADD . .
RUN pip install .

ENTRYPOINT ["libmetric_query"]
