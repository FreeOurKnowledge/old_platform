FROM python:3.6-alpine

WORKDIR /srv

RUN pip install --upgrade pip
RUN apk update 
RUN apk add build-base python-dev py-pip jpeg-dev zlib-dev
RUN apk add --virtual build-deps gcc python3-dev musl-dev
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev py-pillow
RUN apk add postgresql-dev
RUN apk add libffi-dev
RUN apk add libxslt-dev

COPY requirements.txt /srv/requirements.txt
RUN pip install -r /srv/requirements.txt
