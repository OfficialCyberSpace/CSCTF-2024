#!/bin/bash

export FLASK_ENV=production

cd /home/user || exit

python3 -m gunicorn --bind 0.0.0.0:1337 --timeout 120 app.main:app &

python3 -m gunicorn --bind 127.0.0.1:1338 --timeout 120 validation_server.validation:app