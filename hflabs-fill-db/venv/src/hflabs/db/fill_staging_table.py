# -*- coding: utf-8 -*-
import random
from threading import Lock
from threading import Thread

import cx_Oracle

iterations_count = 1
threads_count = 10
records_per_thread = 100000

lock = Lock()


def fill_iterations(count):
    conn = cx_Oracle.connect("AMC_STAGING/amc_test@10.0.61.83:1521/orcl")
    c = conn.cursor()
    for x in range(count):
        c.execute("""INSERT INTO "AMC_STAGING"."ITERATION" (ITERATION_ID, START_TS, ITERATION_DR) VALUES (
        ITERATION_SEQ.nextval, TO_TIMESTAMP('2019-05-28 15:39:42.108000000', 'YYYY-MM-DD HH24:MI:SS.FF'), 'I')""")

    ids = list()
    c.execute("select MAX(ITERATION_ID) from ITERATION")
    for r in c.fetchall():
        ids.append(r[0])

    c.close()
    conn.commit()
    return ids


def staging_records(records_count, iteration_ids, f):
    batch_size = 100
    conn = cx_Oracle.connect("AMC_STAGING/amc_test@10.0.61.83:1521/orcl")
    c = conn.cursor()
    c.prepare(
        """INSERT INTO "AMC_STAGING"."STAGING" (STAGING_ID, ITERATION_ID, RECORD_ID) 
        VALUES (STAGING_SEQ.nextval, :iter_id, :record_id)""")
    insert_data = [{'iter_id': random.choice(iteration_ids), 'record_id': random_word(50)}
                   for i in range(1, batch_size)]

    for x in range(int(records_count / batch_size)):
        c.executemany(None, insert_data)
        print("Written records: %s" % (x * batch_size))
        for e in insert_data:
            write_to_file(f, e['record_id'])

    c.close()
    conn.commit()


def random_word(length):
    letters = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    return ''.join(random.choice(letters) for i in range(length))


def write_to_file(f, text):
    lock.acquire()  # thread blocks at this line until it can obtain lock
    # in this section, only one thread can be present at a time.
    print(text, file=f)
    lock.release()


random.seed()

iter_ids = fill_iterations(iterations_count)
print(iter_ids)
print("fill_iterations is done")

threads = []
file = open("results.txt", 'a+')
for x in range(threads_count):
    thread = Thread(target=staging_records, args=(records_per_thread, iter_ids, file))
    thread.start()
    threads.append(thread)

for th in threads:
    th.join()
