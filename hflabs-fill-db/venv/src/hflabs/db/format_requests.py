# -*- coding: utf-8 -*-
import random
import time

import cx_Oracle

iterations_count = 100
iterations_select_count = 1000
records_count = 10000
records_select_count = 100000


# iterations_count = 10
# iterations_select_count = 100
# records_count = 10
# records_select_count = 100


def get_iterations(count, select_count):
    return _get_ids(count, select_count, "select ITERATION_ID from ITERATION FETCH FIRST :select_count  ROWS ONLY")


def get_records(count, select_count):
    return _get_ids(count, select_count, "select RECORD_ID from STAGING FETCH FIRST :select_count  ROWS ONLY")


def _get_ids(count, select_count, query):
    conn = cx_Oracle.connect("AMC_STAGING/amc_test@10.0.61.83:1521/orcl")
    c = conn.cursor()
    ids = list()
    c.execute(query, select_count=select_count)
    for r in c.fetchall():
        ids.append(r[0])
    c.close()
    conn.commit()

    result = list()
    for r in range(count):
        result.append(random.choice(ids))

    return result


def format_query(iteration_ids, record_ids):
    header = """SELECT
    staging_id
FROM
    amc_staging.staging
WHERE
    iteration_id IN ("""
    infix = ") AND record_id IN ("
    suffix = ");"

    iteration_ids_string = ','.join(str(e) for e in iteration_ids)
    record_ids_string = ','.join("'%s'" % e for e in record_ids)

    return header + iteration_ids_string + infix + record_ids_string + suffix


def temp_table_query(iteration_ids, record_ids):
    header = """CREATE GLOBAL TEMPORARY TABLE amc_staging.temp001 (
    record_id   NVARCHAR2(200)
) ON COMMIT PRESERVE ROWS;
  
"""
    suffix = """select st.STAGING_ID, st.record_id, tm.record_id as s from AMC_STAGING.STAGING st INNER 
    JOIN amc_staging.temp001 tm ON (st.record_id = tm.record_id) ;"""

    record_ids_string = '\n'.join(
        "INSERT INTO amc_staging.temp001 ( record_id ) VALUES ( '%s' );" % e for e in record_ids)

    return header + record_ids_string + suffix


random.seed()
iter_ids = get_iterations(iterations_count, iterations_select_count)
record_ids = get_records(records_count, records_select_count)
# q1 = format_query(iter_ids, record_ids)
q2 = temp_table_query(iter_ids, record_ids)
# print(q1)
print(q2)
