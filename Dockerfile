# Use an official Python runtime as a parent image
FROM python:3.8-bullseye
LABEL maintainer="hello@wagtail.org"

# Set environment varibles
ENV PYTHONUNBUFFERED 1

# Install libenchant and create the requirements folder.
RUN apt-get update -y \
    && apt-get install -y libenchant-2-dev postgresql-client \
    && mkdir -p /code/requirements

# Install the wagtailschedules_demo project's dependencies into the image.
COPY ./wagtailschedules_demo/requirements.txt /code/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install --upgrade pip \
    && pip install -r /code/requirements.txt

# Install wagtailschedules from the host. This folder will be overwritten by a volume mount during run time (so that code
# changes show up immediately), but it also needs to be copied into the image now so that wagtailschedules can be pip install'd.
RUN mkdir /code/wagtailschedules
COPY ./wagtailschedules /code/wagtailschedules/wagtailschedules
COPY ./setup.py /code/wagtailschedules/
COPY ./README.md /code/wagtailschedules/

RUN cd /code/wagtailschedules/ \
    && pip install -e .