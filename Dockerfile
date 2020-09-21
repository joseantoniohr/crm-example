FROM python:3.7-stretch
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
ADD ./requirements.txt /code/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# create unprivileged user
RUN adduser --disabled-password --gecos '' myuser

ADD ./ /code/
RUN apt-get update
RUN apt-get install -y pv

# Necessary for translations
RUN apt-get update && apt-get install -y gettext libgettextpo-dev
