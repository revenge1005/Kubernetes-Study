FROM ubuntu:18.04
RUN apt-get update && apt-get install -y curl apt-transport-https gnupg2

# pyhon
RUN apt-get install -y python python-pip
RUN pip install kubernetes

COPY main.py /main.py

WORKDIR /
CMD python /main.py

