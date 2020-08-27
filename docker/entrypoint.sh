#!/bin/sh

/src/manage.py migrate --noinput

# TODO: figure out why the fixture is failing
# /src/manage.py generatefakedata

/src/manage.py startserver 0.0.0.0:8080
