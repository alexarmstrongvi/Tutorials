#!/usr/bin/env python
"""
Example script for logging in a multiprocessing pool context
"""
# Standard library
import concurrent.futures as cf
import functools
import logging
import logging.handlers
import multiprocessing as mp
from multiprocessing.process import BaseProcess
import random
import re
import threading
import time
from typing import Optional

# Globals
log = logging.getLogger(__name__)

cfg = {
    "n_tasks": 3,
    "n_processes": 2,
    "logging": {
        "level": "DEBUG",
        "format": "%(levelname)8s | [%(processName)s] %(module)s :: %(message)s",
    },
}


################################################################################
def main_pool():
    my_args1 = range(cfg["n_tasks"])
    my_args2 = reversed(range(cfg["n_tasks"]))
    basic_config = cfg["logging"]
    set_process_name(mp.current_process())

    with mp.Manager() as manager:
        # NOTE: The Manager starts its own child process so child processes in
        # the pool will start with a number ID of 2
        queue = manager.Queue(-1)

        # Configure main process logging
        # Option 1: Logging handled in main process by thread
        log_listener = threading.Thread(
            target=start_log_listener, args=(queue, basic_config)
        )
        log_listener.start()
        # Option 2: Logging handled by child process
        # log.addHandler(logging.handlers.QueueHandler(queue))

        # Combine/Simplify inputs for multiprocessing
        mp_configure_logging_partial = functools.partial(
            mp_configure_logging,
            queue=queue,
            log_level=basic_config["level"],
        )

        def noisy_mp_iterable():
            # For demoing which functions support lazy evaluation
            for x, y in zip(my_args1, my_args2):
                log.info("Generating args = %s", (x, y))
                time.sleep(random.random())
                yield x, y

        mp_iterable = noisy_mp_iterable()
        # mp_iterable = zip(my_args1, my_args2)

        log.info("Starting worker pool")
        # Option A: multiprocessing Pool
        with mp.Pool(
            processes=cfg["n_processes"],
            initializer=_mp_initalizer,
            initargs=(mp_configure_logging_partial,),
        ) as pool:
            # Option 2: Logging handled by child process
            # pool.apply_async(start_log_listener, args=(queue, basic_config))

            log.info("Starting %d worker processes", pool._processes)
            # Option I: Get results as they complete
            results = pool.imap_unordered(_mp_pow, mp_iterable)
            # Option II: Get results in order after generating all input arguments
            # results = pool.map(_mp_pow, mp_iterable)
            # Option III: Get results in order with lazy generator evaluation
            # results = pool.imap(_mp_pow, mp_iterable)

            for args, result in results:
                log.info("Got result: pow%s = %s", args, result)

        # Option B: concurrent.futures ProcessPoolExecutor
        # with cf.ProcessPoolExecutor(
        #     max_workers = cfg["n_processes"],
        #     initializer = _mp_initalizer,
        #     initargs    = (mp_configure_logging_partial,)
        # ) as executor:
        #     # Option I: Get results as the complete
        #     futures = [executor.submit(_mp_pow, arg) for arg in mp_iterable]
        #     results = (future.result() for future in cf.as_completed(futures))
        #     # Option II: Get results in order
        #     # results = executor.map(_mp_pow, mp_iterable)

        #     # Do something with results
        #     for arg, result in results:
        #         log.info("Got result: pow%s = %s", arg, result)

        queue.put_nowait(None)
        log_listener.join()
        log.info("Main process done")


def main_manual():
    basic_config = cfg["logging"]
    set_process_name(mp.current_process())
    queue = mp.Queue(-1)

    log_listener = threading.Thread(
        target=start_log_listener, args=(queue, basic_config)
    )
    log_listener.start()

    mp_configure_logging_partial = functools.partial(
        mp_configure_logging,
        queue=queue,
        log_level=basic_config["level"],
    )

    # Create Process instances
    workers = []
    worker = mp.Process(
        target=_mp_target_pow, args=(mp_configure_logging_partial, 2, 3)
    )
    workers.append(worker)

    worker = mp.Process(
        target=_mp_target_pow, args=(mp_configure_logging_partial, 4, 5)
    )
    workers.append(worker)

    log.debug("Starting worker processes")
    for worker in workers:
        worker.start()

    log.debug("Waiting for worker processes...")
    for worker in workers:
        worker.join()

    # Shutdown
    log.debug("Shutting down")
    queue.put_nowait(None)
    log_listener.join()
    log.info("Done")


# Use-case specific wrappers to standardize calls to multiprocessing API
def _mp_pow(args):
    """Wrapper of worker function to handle input arg(s) and return value(s)

    1) Accepts a single input parameter but handles unpacking iterables for the
    worker function. While some of the multiprocessing functions can handle
    multiple arguments (e.g. pool.starmap, executor.map), other's don't and my
    preference is to keep a common convention across use cases.
    2) Returns some or all of the input arguments alongside the result in case
    results are being collected out of order.
    """
    arg1, arg2 = args
    return args, pow(num1=arg1, num2=arg2)


def _mp_initalizer(configure_logging):
    """Run all initialization steps for child processes"""
    set_process_name()
    configure_logging()


def _mp_target_pow(configure_logging, *args, **kwargs):
    """Run initialization steps for child process before worker target

    This is only useful for manually created Process instances that do not have
    an initializer parameter like Pool.
    """
    _mp_initalizer(configure_logging)
    return pow(*args, **kwargs)


################################################################################
# Generally useful functions
def set_process_name(process: Optional[BaseProcess] = None):
    if process is None:
        process = mp.current_process()

    if process.name == "MainProcess":
        process.name = "P0"
    else:
        process.name = re.sub(
            r"^(?:SpawnPoolWorker|SpawnProcess|Process)-", "P", process.name
        )


def mp_configure_logging(queue, log_level):
    """Configure logging in child processes"""
    root = logging.root
    root.addHandler(logging.handlers.QueueHandler(queue))
    root.setLevel(log_level)
    log.debug("Logging configured")


def start_log_listener(queue, basic_config):
    logging.basicConfig(**basic_config)
    log.debug(f"Log listener configured")

    while True:
        if (record := queue.get()) is None:
            log.info(f"Logger process shutting down.")
            break
        logging.getLogger(record.name).handle(record)


################################################################################
# Business logic
def pow(num1, num2):
    log.debug("Starting. args = %s", (num1, num2))
    time.sleep(random.random())
    log.debug("Done")
    return num1**num2


################################################################################
if __name__ == "__main__":
    print("Demoing process pool")
    main_pool()
    print("\n" + "=" * 80)

    print("Demoing manual process handling")
    main_manual()
    print("\n")
