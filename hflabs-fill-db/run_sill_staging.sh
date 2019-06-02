#!/usr/bin/env bash
cd venv
export LD_LIBRARY_PATH=instantclient_19_3:${LD_LIBRARY_PATH}
source ./bin/activate
python ./hflabs/db/fill_staging_table.py