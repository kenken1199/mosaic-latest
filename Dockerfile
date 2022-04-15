FROM python:3

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libgl1-mesa-dev

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
ADD . /code/
