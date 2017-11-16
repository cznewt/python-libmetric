FROM python:2.7-jessie

RUN apt-get update && apt-get -y install build-dep python-lxml
RUN pip install libmetric

ENTRYPOINT ["instant_alarm"]
