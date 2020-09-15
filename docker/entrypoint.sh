#!/bin/sh

/src/manage.py migrate --noinput
/src/manage.py generatefakedata
/src/manage.py runserver 0.0.0.0:8080
