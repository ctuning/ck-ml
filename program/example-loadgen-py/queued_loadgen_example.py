#!/usr/bin/env python3

import array
import os
import random
import time

import numpy as np
import mlperf_loadgen as lg

import queue
import threading


## LoadGen test properties:
#
LOADGEN_SCENARIO        = os.getenv('CK_LOADGEN_SCENARIO', 'SingleStream')
LOADGEN_MODE            = os.getenv('CK_LOADGEN_MODE', 'AccuracyOnly')
LOADGEN_BUFFER_SIZE     = int(os.getenv('CK_LOADGEN_BUFFER_SIZE'))          # set to how many samples are you prepared to keep in memory at once
LOADGEN_DATASET_SIZE    = int(os.getenv('CK_LOADGEN_DATASET_SIZE'))         # set to how many total samples to choose from (0 = full set)
LOADGEN_COUNT_OVERRIDE  = os.getenv('CK_LOADGEN_COUNT_OVERRIDE', '')        # if not set, use value from LoadGen's config file
LOADGEN_MULTISTREAMNESS = os.getenv('CK_LOADGEN_MULTISTREAMNESS', '')       # if not set, use value from LoadGen's config file
#
MLPERF_CONF_PATH        = os.environ['CK_ENV_MLPERF_INFERENCE_MLPERF_CONF']
USER_CONF_PATH          = os.environ['CK_LOADGEN_USER_CONF']
#
MODEL_NAME              = os.environ['ML_MODEL_MODEL_NAME']                 # an obligatory input parameter for now


## Specific for this example:
#
LATENCY_S          = float(os.environ['CK_EXAMPLE_LATENCY_MS'])/1000        # fractional seconds
BATCH_CAPACITY      = int(os.environ['CK_EXAMPLE_BATCH_CAPACITY'])          # model's property
TOPUP_TIME_S        = float(os.environ['CK_EXAMPLE_TOPUP_TIME_MS'])/1000    # fractional seconds


## Global input data and expected labels:
#
dataset                 = [10*i for i in range(LOADGEN_DATASET_SIZE)]
labelset                = [10*i+random.randint(0,1) for i in range(LOADGEN_DATASET_SIZE)]

## Global queue:
#
task_queue              = queue.Queue(100)  # sent by issue_queries(), received by the worker


def predict_labels(batch_inputs):
    time.sleep(LATENCY_S)
    results = [int(one_input/10)+1 for one_input in batch_inputs]
    return results


def worker_code():
    while True:
        ## Grab a new batch:
        #
        grabbed_count   = 0
        deadline_ts     = None
        batch_jobs      = []
        batch_inputs    = []
        for grabbed_count in range(BATCH_CAPACITY):  # may not run to the end due to the cumulative timeout
            try:
                grab_timeout    = None if deadline_ts==None else max(0, deadline_ts - time.time())    # no waiting limit on the first job
                job             = task_queue.get(timeout = grab_timeout)

                batch_jobs.append(job)
                batch_inputs.append(job['inputs'])

                if grabbed_count==0:
                    deadline_ts = job['ts_submitted'] + TOPUP_TIME_S

            except queue.Empty:
                break   # we ran out of TOPUP_TIME_S

        print(f"LG: worker grabbed and submitted {len(batch_jobs)} jobs")

        ## Predict the whole batch:
        #
        predicted_labels    = predict_labels(batch_inputs)   # takes LATENCY_S of time
        ts_predicted        = time.time()

        ## Report batch results:
        #
        for index_in_batch, job in enumerate(batch_jobs):
            predicted_label = predicted_labels[index_in_batch]
            one_input       = job['inputs']
            query_sample    = job['query_sample']
            ts_submitted    = job['ts_submitted']
            print(f"LG: worker predicted: for input={one_input} label={predicted_label} in {(ts_predicted-ts_submitted)*1000} ms")

            response_array = array.array("B", np.array(predicted_label, np.float32).tobytes())
            bi = response_array.buffer_info()
            response = lg.QuerySampleResponse(query_sample.id, bi[0], bi[1])
            lg.QuerySamplesComplete([response])

            task_queue.task_done()


def issue_queries(query_samples):

    printable_query = [(qs.index, qs.id) for qs in query_samples]
    print("LG: issue_queries( {} )".format(printable_query))

    for query_sample in query_samples:

        job_inputs  = dataset[query_sample.index]

        submitted_job = {
            'query_sample':     query_sample,
            'inputs':           job_inputs,
            'ts_submitted':     time.time(),
        }
        task_queue.put(submitted_job)


def flush_queries():
    print("LG called flush_queries()")

def process_latencies(latencies_ns):
    latencies_ms = [ (ns * 1e-6) for ns in latencies_ns ]
    print("LG called process_latencies({})".format(latencies_ms))

    if LOADGEN_SCENARIO == 'Offline':
        latencies_ms   = (np.asarray(latencies_ms) - np.asarray([0] + latencies_ms[:-1])).tolist()
        print("Offline latencies transformed to absolute time: {}".format(latencies_ms))

    latencies_size      = len(latencies_ms)
    latencies_avg       = int(sum(latencies_ms)/latencies_size)
    latencies_sorted    = sorted(latencies_ms)
    latencies_p50       = int(latencies_size * 0.5);
    latencies_p90       = int(latencies_size * 0.9);
    latencies_p99       = int(latencies_size * 0.99);

    print("--------------------------------------------------------------------")
    print("|                LATENCIES (in milliseconds and fps)               |")
    print("--------------------------------------------------------------------")
    print("Number of samples run:       {:9d}".format(latencies_size))
    print("Min latency:                 {:9.2f} ms   ({:.3f} fps)".format(latencies_sorted[0], 1e3/latencies_sorted[0]))
    print("Median latency:              {:9.2f} ms   ({:.3f} fps)".format(latencies_sorted[latencies_p50], 1e3/latencies_sorted[latencies_p50]))
    print("Average latency:             {:9.2f} ms   ({:.3f} fps)".format(latencies_avg, 1e3/latencies_avg))
    print("90 percentile latency:       {:9.2f} ms   ({:.3f} fps)".format(latencies_sorted[latencies_p90], 1e3/latencies_sorted[latencies_p90]))
    print("99 percentile latency:       {:9.2f} ms   ({:.3f} fps)".format(latencies_sorted[latencies_p99], 1e3/latencies_sorted[latencies_p99]))
    print("Max latency:                 {:9.2f} ms   ({:.3f} fps)".format(latencies_sorted[-1], 1e3/latencies_sorted[-1]))
    print("--------------------------------------------------------------------")


def load_query_samples(sample_indices):
    print("LG called load_query_samples({})".format(sample_indices))

def unload_query_samples(sample_indices):
    print("LG called unload_query_samples({})".format(sample_indices))
    print("")


def benchmark_using_loadgen():
    "Perform the benchmark using python API for the LoadGen library"

    scenario = {
        'SingleStream':     lg.TestScenario.SingleStream,
        'MultiStream':      lg.TestScenario.MultiStream,
        'Server':           lg.TestScenario.Server,
        'Offline':          lg.TestScenario.Offline,
    }[LOADGEN_SCENARIO]

    mode = {
        'AccuracyOnly':     lg.TestMode.AccuracyOnly,
        'PerformanceOnly':  lg.TestMode.PerformanceOnly,
        'SubmissionRun':    lg.TestMode.SubmissionRun,
    }[LOADGEN_MODE]

    ts = lg.TestSettings()
    ts.FromConfig(MLPERF_CONF_PATH, MODEL_NAME, LOADGEN_SCENARIO)
    ts.FromConfig(USER_CONF_PATH, MODEL_NAME, LOADGEN_SCENARIO)
    ts.scenario = scenario
    ts.mode     = mode

    sut = lg.ConstructSUT(issue_queries, flush_queries, process_latencies)
    qsl = lg.ConstructQSL(LOADGEN_DATASET_SIZE, LOADGEN_BUFFER_SIZE, load_query_samples, unload_query_samples)

    worker_thread = threading.Thread(target=worker_code, daemon=True)
    worker_thread.start()

    log_settings = lg.LogSettings()
    log_settings.enable_trace = False
    lg.StartTestWithLogSettings(sut, qsl, ts, log_settings)

    task_queue.join()   # wait for the task_queue to complete, but not for the (daemonized) worker thread

    lg.DestroyQSL(qsl)
    lg.DestroySUT(sut)


try:
    benchmark_using_loadgen()
except Exception as e:
    print(str(e))
