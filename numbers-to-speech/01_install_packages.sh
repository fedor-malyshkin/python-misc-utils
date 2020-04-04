#!/bin/sh

. venv/bin/activate && pip3 install gTTS \
 && pip3 install playsound \
 && pip3 install vext \
 && pip install vext.gi \
 && pip install inflect \
 && pip install Faker
