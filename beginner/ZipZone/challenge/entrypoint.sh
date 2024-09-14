#!/bin/bash

mkdir /tmp/raw /tmp/files
cp /home/user/flag.txt /tmp/flag.txt
cd /home/user || exit
python3 -m gunicorn --bind 0.0.0.0:1337 --timeout 120 app:app
