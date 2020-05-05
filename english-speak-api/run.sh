#!/bin/sh

. venv/bin/activate
export FLASK_ENV=development
export FLASK_APP=./english/speak
python -m flask run --host=0.0.0.0
