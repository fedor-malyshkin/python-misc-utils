#!/bin/sh
source venv/bin/activate

for i in $(seq 10)
do
 python ./src/english/numbers/run.py -n 4
 sleep 1;
done
