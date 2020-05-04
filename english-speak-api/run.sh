#!/bin/sh

. venv/bin/activate
export FLASK_APP=./src/english/speak/main.py
python -m flask run
