ARG BASE_IMAGE_VERSION
FROM python:$BASE_IMAGE_VERSION-slim-buster as build

RUN apt update -qq
RUN apt install git -y
RUN apt install curl -y
RUN apt install gcc -y
RUN apt install g++ -y
RUN apt install make -y
RUN apt install file -y
RUN apt install musl-dev -y
RUN apt install libffi-dev -y
RUN apt install zlib1g -y
RUN apt install zlib1g-dev -y
RUN apt install libpq-dev -y
RUN apt install python-dev -y

COPY docker/get-poetry.py get-poetry.py
RUN POETRY_VERSION=1.1.13 python3 get-poetry.py

WORKDIR /usr/src/app/
ADD poetry.lock pyproject.toml ./
RUN $HOME/.poetry/bin/poetry install

ADD src src
ADD config config
ADD run.py VERSION ./
RUN $HOME/.poetry/bin/poetry run pyinstaller run.py -n rubix-data-push --clean --onefile \
    --add-data pyproject.toml:. \
    --add-data VERSION:. \
    --add-data config:config

FROM python:$BASE_IMAGE_VERSION-slim

ARG MAINTAINER="zero88 <sontt246@gmail.com>"
ARG APP_VERSION="1.0.0"
ARG RUBIX_UID=642
ARG NUBEIO_GID=1173
ARG COMMIT_SHA=$COMMIT_SHA

LABEL maintainer=$MAINTAINER version=$APP_VERSION commit=$COMMIT_SHA

ENV RUBIX_VOLUME=/data/rubix-data-push

RUN groupadd -g $NUBEIO_GID nubeio \
    && useradd -u $RUBIX_UID -G nubeio rubix \
    && mkdir -p $RUBIX_VOLUME \
    && chown -R rubix:nubeio $RUBIX_VOLUME

WORKDIR /usr/src/app/
COPY --chown=rubix:nubeio --from=build /usr/src/app/dist/rubix-data-push ./

USER rubix:nubeio

VOLUME $RUBIX_VOLUME

EXPOSE 2020

ENTRYPOINT [ "./rubix-data-push" ]
