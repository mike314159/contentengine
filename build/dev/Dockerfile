
# Fragment of Dockerfile used in dev and prod builds

# pull official base image https://hub.docker.com/_/python
FROM python:3.11.4-bookworm

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y --no-install-recommends gcc

# RUN apt-get install -y ffmpeg

# Need this for building some dependencies like duckdb
RUN apt-get install -y g++

# Install cron
RUN apt-get update && apt-get install cron -y

RUN pip install --upgrade pip
RUN pip install flake8==5.0.4
RUN flake8 --ignore=E501,F401 .

# Optional: install pipx or uv
RUN pip install --user aider

# Make sure /root/.local/bin is in the PATH
ENV PATH="/root/.local/bin:${PATH}"

# install python dependencies
#COPY requirements.txt /tmp/requirements.txt
#RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r /tmp/requirements.txt

COPY requirements.txt /
COPY entrypoint.sh /

RUN pip install -r /requirements.txt

# Source: Dockerfile.dev
# Fragment of Dockerfile used in dev build


CMD [ "/entrypoint.sh" ]