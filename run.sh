#!/usr/bin/env bash

set -e

if [ ! -d env ]; then
    virtualenv env -ppython3.6
    . env/bin/activate
    pip install -r requirements.txt
    ./manage.py migrate
else
    . env/bin/activate
fi

./manage.py runserver 0.0.0.0:8000
