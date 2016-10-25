#!/usr/bin/env python

__author__ = 'brianoneill'
__version__ = '0.2'

import os
import time
import math
import logging
from multiprocessing import Process, JoinableQueue

try:
    import prelogging
except ImportError:
    import sys
    sys.path[0:0] = ['..']
from prelogging import LCDict

# Py2 stupidity:
import sys
if sys.version_info.major > 2:
    # NUM_PROCESSES = max(os.cpu_count() - 2, 1)
    NUM_PROCESSES = os.cpu_count()
else:
    NUM_PROCESSES = 4

from examples._get_locking_pref import get_locking_pref

LOG_PATH = '_log/mproc'


def extract_document_data_in_range(docs, start_doc_num, end_doc_num,
                                   out_q,   # : JoinableQueue,
                                   process_num):
    """
    Process docs[start_doc_num: end_doc_num].
    :param docs:
    :param start_doc_num:
    :param end_doc_num:
    :param out_q:
    :param process_num:
    :return:
    """
    logging.getLogger(__name__).info(">>>>>> Hi from process-%d; "
                                     "processing docs %d - %d"
                                     % (process_num + 1, start_doc_num, end_doc_num - 1))
    processed_docs_for_proc = []

    # For PY2:
    start_doc_num = int(start_doc_num)
    end_doc_num = int(end_doc_num)

    for x in docs[start_doc_num: end_doc_num]:
        pair = (process_num + 1, x)
        processed_docs_for_proc.append(pair)
        logging.getLogger(__name__).info("%d: %2d\n\tand again %d: %2d" % (pair + pair))
        if x % 2 == 0:
            time.sleep(0.05 * (process_num % 2 + 1))

    logging.getLogger(__name__).info(">>>>>> Bye from process-%d" % (process_num + 1))

    out_q.put(processed_docs_for_proc)


def extract_document_data_multiprocess(docs):
    """:param docs: list"""

    #---------------------------------------------------------
    # Fire up the processes
    #---------------------------------------------------------
    # Use limit and offset to subset the query results.
    # Figure out this process's range of docs to process
    chunksize = math.ceil(NUM_DOCS_TOTAL / NUM_PROCESSES)
    # Subdivisions:
    #  [0, chunksize)
    #  [chunksize, 2 * chunksize)
    #   ...
    #  [(NUM_DOCS_TOTAL-1) * chunksize, min(num_records, NUM_DOCS_TOTAL * chunksize))

    output_queue = JoinableQueue()

    for i in range(NUM_PROCESSES):
        start_doc_num = i * chunksize
        start_doc_num_next_chunk = min((i + 1) * chunksize, len(docs))

        p = Process(target=extract_document_data_in_range,
                    args=(docs, start_doc_num, start_doc_num_next_chunk,
                          output_queue,
                          i)              # process_num
        )
        p.start()

    #---------------------------------------------------------
    # Aggregate all results into single results, return those.
    #---------------------------------------------------------
    processed_docs = []

    for i in range(NUM_PROCESSES):
        proc_results = output_queue.get()
        # proc_results is a list of pairs (j,x), (j, x+1),  .. (j, x+K)
        # with 0 <= x < NUM_DOCS_TOTAL, 0 <= j < NUM_PROCESSES
        processed_docs.extend(proc_results)
        output_queue.task_done()

    output_queue.join()

    return processed_docs


def config_logging(use_locking):
    """
    """
    logfilename = ('mproc_LOCKING.log' if use_locking else 'mproc_NOLOCKING.log')
    # add handlers to root == False, default
    lcd = LCDict(log_path=LOG_PATH,
                 locking=use_locking)

    ## Add 'console' handler with level higher than 'DEBUG';
    # add main file handler, which will write to '_log/' + logfilename;
    # add logger that uses them.
    lcd.add_stdout_handler(
        'console',
        formatter='msg',
        level='INFO'
    ).add_formatter(
        'my_file_formatter',
        format='%(processName)-12s: %(name)-14s: %(levelname)-8s: %(asctime)24s: %(message)s',
    ).add_file_handler(
        'app_file',
        filename=logfilename,
        mode='w',
        level='DEBUG',
        formatter='my_file_formatter'
    ).add_logger(
        __name__,
        handlers=('app_file', 'console'),
        level='DEBUG',
        propagate=False    # so it DOESN'T propagate to root logger
    )
    lcd.config()


NUM_DOCS_TOTAL = 80     # 64


def main(use_locking=None):
    if use_locking is None:
        use_locking = get_locking_pref()

    config_logging(use_locking)

    docs = list(range(NUM_DOCS_TOTAL))

    # print("Processing %d documents using %d processes." %
    #       (NUM_DOCS_TOTAL, NUM_PROCESSES))
    logging.getLogger(__name__).info(
        "Processing %d documents using %d processes." %
        (NUM_DOCS_TOTAL, NUM_PROCESSES))

    # start_time = time.perf_counter()
    total_results = extract_document_data_multiprocess(docs)
    # elapsed_time = time.perf_counter() - start_time

    logging.getLogger(__name__).info(
        "NUM_DOCS_TOTAL: %d, len(total_results): %d"
        % (NUM_DOCS_TOTAL, len(total_results)))
    logging.getLogger(__name__).info(total_results)


if __name__ == '__main__':
    # main(use_locking=True)
    # main(use_locking=False)
    main()
