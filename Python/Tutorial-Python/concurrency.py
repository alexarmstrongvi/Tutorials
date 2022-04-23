#!/usr/bin/env python3
################################################################################
#
# Notes
#   * CPU-bound vs I/O-bound
#   * Concurrency -
#       * Multitasking - switiching between tasks on a single processor
#           * pre-emptive (`threading`) - OS forces switching decision
#           * cooperative (`asyncio`) - tasks give up control to allow switching by manager
#       * Multiprocessing (`multiprocessing`) - running processes in parallel on multiple processors
#   * Thread vs task vs process
#       * Thread-pool
#       * Executor
#   * Awaitables - any object that can be awaited on with 'await'
#       * Types
#           * Coroutine - an object that can be scheduled to run asychronously
#               * coroutine function - a function defined with 'async'
#               * coroutine object - the object returned by calling a coroutine function
#           * Task - a wrapped coroutine that is scheduled to run asap
#           * Future -
#       * Running coroutine
#           * asyncio.run()
#           * await
#   * Thread-safety and race conditions
#       * Race condition - the condition of multiple threads in a program racing to read from and write to a shared resource, resulting in undefined behavior (e.g. crashing or at least non-determinism).
#       * Thread-safety - the state of a procedure that can be run within a thread such that it will behave in a well defined way
#
# References
# * Official Docs : https://docs.python.org/3/library/concurrency.html
# * Official Docs : https://docs.python.org/3/library/asyncio.html
# * Real Python : https://realpython.com/python-concurrency/
# * Stackoverflow : https://stackoverflow.com/questions/49005651/how-does-asyncio-actually-work
################################################################################
import time
import types
import concurrent.futures
import threading
import asyncio
import multiprocessing
from typing import Callable, Awaitable, Any
from statistics import mean

# Processes created by multiprocessing import __main__ so be cautious about globals
#print(f'Loading concurrency.py from {__name__}')
if __name__ == '__mp_main__':
    curr_proc = multiprocessing.current_process()
    print(f'Spawning process {curr_proc.name} (PID {curr_proc.pid})')

# Configuration
n_inputs  = 7
max_threads = 3
n_processes = 4
n_processors = min(4, multiprocessing.cpu_count())
slow_io_delay = 0.1
really_long_time = 10**10

get_methods = lambda mod : [x for x in dir(mod) if not x.startswith('_')]
################################################################################
# Basic usage
################################################################################
############################################################
# Threading
def simple_synchronous_tasking(inputs: list[Any]) -> list[Any]:
    result = map(thread_func, inputs)
    return list(result)

def simple_preemptive_multitasking(inputs: list[Any], max_threads: int) -> list[Any]:
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        result = executor.map(thread_func, inputs)
    return list(result)

def simple_cooperative_multitasking(inputs: list[Any], max_threads: int) -> list[Any]:
    awaitable = task_runner(inputs, max_threads)
    result = asyncio.run(awaitable)
    return result

async def task_runner(
    task_inputs: list[Any],
    max_threads: int = None
) -> Awaitable[list[Any]]:
    awaitables = [coroutine_func(x) for x in task_inputs]
    if max_threads is None:
        result = await asyncio.gather(*awaitables, return_exceptions=True)
    else:
        # Requires jumping through more hoops to limit task count
        result = await limited_gather(max_threads, *awaitables, return_exceptions=True)
    return result

async def limited_gather(
    max_threads : int,
    *aws        : list[Callable[..., Awaitable]],
    **kwargs    : dict[str, Any],
) -> asyncio.Future[Any]:
    # See https://stackoverflow.com/questions/48483348/how-to-limit-concurrency-with-python-asyncio
    semaphore = asyncio.Semaphore(max_threads)
    async def sem_aw(awaitable):
        async with semaphore:
            return await awaitable
    sem_aws = (sem_aw(aw) for aw in aws)
    print(f'Controlled gather with max {max_threads} threads')
    return await asyncio.gather(*sem_aws, **kwargs)

# Dummy thread functions
def thread_func(x: Any) -> Any:
    thread = threading.current_thread()
    thread_num = get_thread_num(thread)
    print(f"Thread {thread_num}) Start: input = {x}")

    result = slow_io_process(x)

    print(f"Thread {thread_num}) Done")

    return result

def slow_io_process(x: Any) -> str:
    time.sleep(slow_io_delay)
    return repr(x)

async def coroutine_func(x: Any) -> Any:
    #task = asyncio.Task.current_task()
    task_name = '#' #task.get_name()
    print(f"Task {task_name}) Start: input = {x}")

    result = await slow_aio_process(x)

    print(f"Task {task_name}) Done")

    return result

async def slow_aio_process(x: Any) -> str:
    await asyncio.sleep(slow_io_delay)
    return repr(x)

# Utilities
def get_thread_num(thread: threading.Thread) -> int:
    if thread.name.startswith('ThreadPoolExecutor'):
        # Example: ThreadPoolExecutor-0_11
        # user_prefix = int(thread.name.split('-')[1].split('_')[0])
        return int(thread.name.split('_')[1])
    elif thread.name == 'MainThread':
        return 0
    raise NotImplementedError(f'Unknown thread name: {thread.name}')

############################################################
# Multiprocessing
def slow_cpu_process(x):
    print(f'Running slow cpu process {x}')
    start = time.time()
    _ = [n*2 for n in range(2 * 10**7)]
    return round(time.time() - start,3)

# Synchronous version
def simple_synchronous_processing():
    result = [slow_cpu_process(n) for n in range(n_processes)]
    print(result)

def simple_multiprocessing():
    with multiprocessing.Pool() as pool:
        result = pool.map(slow_cpu_process, range(n_processes))
    print(result)

################################################################################
# Advanced asyncio
################################################################################
async def say_after(msec, say):
    await asyncio.sleep(msec/1000)
    print(say)

async def return_after(msec, return_val):
    await asyncio.sleep(msec/1000)
    return return_val

async def advanced_cooperative_multitasking():
    # This will run right away since it is a regular function (i.e. not a coroutine)
    print('1')

    # This returns a coroutine object that is never awaited and so never runs.
    # It produces a RuntimeWarning so uncomment if you want.
    # coro_obj_never_awaited = say_after(0,'X')

    # This returns a coroutine that is awaited and so runs to completion.
    coro_obj = say_after(0,'2')
    assert isinstance(coro_obj, types.CoroutineType)
    await coro_obj

    # It is rarely necessary to create a reference to the coroutine object.
    # Usually, you just await the function call.
    await say_after(0,'3')

    # Coroutine objects can be created and then awaited in whatever order you want
    coro_obj1 = say_after(0,'5')
    coro_obj2 = say_after(0,'4')
    await coro_obj2
    await coro_obj1

    # Note that awaiting does not lead to things running concurrently. It is
    # telling the event loop in charge of running the encapsulating coroutine
    # function (i.e. advanced_cooperative_multitasking) that the function is
    # going to wait for this process to finish before moving on to run later
    # lines of code. More specifically, it yields control back to the event loop
    # so that the event loop can start running other coroutines if it wants.
    # When the await statement finishes, the function will request control back
    # from the event loop. Once that happens, the function will continue on.
    coro_obj1 = say_after(1,'6')
    coro_obj2 = say_after(0,'7')
    await coro_obj1 # Waiting to finish before running coro_obj2
    await coro_obj2

    # If you want to run things concurrently, you need to schedule the
    # coroutines with tasks. The coroutine will start running and the program
    # will move on to process later lines.
    asyncio.create_task(say_after(1, '9'))
    asyncio.create_task(say_after(0, '8'))
    # Even though we don't have to await tasks in order them to run, let's
    # manually wait for the tasks to finish before moving forward. Otherwise, it
    # might print its message while later commands are running.
    await asyncio.sleep(0.001)
    # If we don't await the task and the program happens to finish running
    # before that task is complete, the task is cancelled during garbage
    # collection and any results are lost.
    asyncio.create_task(say_after(really_long_time, 'X'))

    # Saving a variable reference to the task gives us some control over the
    # task while it runs.
    task = asyncio.create_task(say_after(really_long_time, 'X'), name='my_task_name')
    assert isinstance(task, asyncio.Task)
    assert task.get_name()  == 'my_task_name'
    task.set_name('my_new_task_name')
    assert task.get_name()  == 'my_new_task_name'
    assert task.done()      is False
    assert task.cancelled() is False
    task.cancel() # The task is taking too long
    await asyncio.sleep(0.001) # Wait for cancel signal to reach the task
    assert task.done()      is True
    assert task.cancelled() is True

    # It is rarely necessary to manually create the tasks. Instead, multiple
    # coroutine objects can be scheduled as tasks using gather(), which returns
    # a future object. Awaiting that future object will wait for all tasks to be
    # done.
    my_coroutine_objects = [
            # The coroutine objects will be scheduled in the order they are provided
            say_after(2,'13'),
            say_after(0,'10'),
            say_after(1,'12'),
            say_after(0,'11'), # So this should always finish second
    ]
    future = asyncio.gather(*my_coroutine_objects)
    assert isinstance(future, asyncio.Future)
    await future

    print('Done')

    # What about if we want the coroutines to return something?
    # The syntax is pretty straightforward for regular coroutines
    coro_obj = return_after(0, 'success')
    result = await coro_obj
    assert result == 'success'

    # The above can be condensed down
    result = await return_after(0, 'success')
    assert result == 'success'

    # For tasks you can access the result with the result() method
    task = asyncio.create_task(return_after(0, 'success'))
    await task
    result = task.result()
    assert result == 'success'

    # This too can be condensed to two or even one line
    task = asyncio.create_task(return_after(0, 'success'))
    result = await task
    assert result == 'success'

    result = await asyncio.create_task(return_after(0, 'success'))
    assert result == 'success'

    # Make sure to wait for the task to finish before trying to get the result
    exception_raised = False
    try:
        task = asyncio.create_task(return_after(0, 'success'))
        task.result()
    except asyncio.exceptions.InvalidStateError:
        exception_raised = True
    assert exception_raised

    # Future objects obtained via gather() will return the results as a list in
    # the order the coroutine objects were provided. The future is not done
    # until all tasks are done.
    my_coroutine_objects = [
        return_after(2,'A'),
        return_after(0,'B'),
        return_after(1,'C'),
        return_after(0,'D')
    ]
    result = await asyncio.gather(*my_coroutine_objects)
    assert result == ['A','B','C','D']

    # What if we want to access the results as they finish? In that case the
    # coroutines should be used within another coroutine. The gather step is for
    # use at the level where the program cannot progress until all tasks are
    # complete.

    # Shielding (asyncio.shield)
    # Timeouts (asycio.wait_for)
    # Waiting (asyncio.wait)
    # Running in threads (asyncio.to_thread)
    return

async def test_read_and_write():
    # How to read from multiple files at once and write to a single file
    async def read_and_write_after(msec, ifile, ofile):
        text = await slow_file_read(msec, ifile)
        text = process_text(text)
        write_to_file(text, ofile)

    async def slow_file_read(msec, ifile_path):
        with open(ifile_path, 'r') as ifile:
            await asyncio.sleep(msec/1000)
            text = ifile.read()
        return text

    def process_text(text):
        return 'Processed ' + text

    def write_to_file(text, ofile_path):
        with open(ofile_path, 'a+') as ofile:
            #time.sleep(0.001)
            ofile.write(text)

    coro_objs = [
        read_and_write_after(1,'test_files/input_file1.txt', 'output_file.txt'),
        read_and_write_after(0,'test_files/input_file2.txt', 'output_file.txt'),
        read_and_write_after(3,'test_files/input_file3.txt', 'output_file.txt'),
        read_and_write_after(2,'test_files/input_file4.txt', 'output_file.txt'),
    ]

    await asyncio.gather(*coro_objs)
    with open('output_file.txt','r') as ifile:
        print(ifile.read())

################################################################################
# Advanced threading
################################################################################
# Thread safety (Locks, local())

# Example race condition
n_race_inputs = 1000 # Vary this to change behavior (small values give wierdly regular behavior)
n_races = 9 # More races increases chances of different behavior

shared_resource = None
race_inputs = list(range(1, n_race_inputs+1))

def modify_shared_resource(x):
    global shared_resource
    shared_resource = x

def example_race_condition():
    print('\nRace condition')
    results = []
    for _ in range(n_races):
        shared_resource = -1
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
            executor.map(modify_shared_resource, race_inputs)
            results.append(shared_resource)
    print(f'Last of {n_race_inputs} inputs processed by {max_threads} threads:')
    for ii, result in enumerate(results):
        print(f'\tRace {ii+1}) Input {result}')

#import threading
#lock = Lock()
#thread_local = threading.local()

########################################
# Manually starting threads
# t1 = threading.Thread(target=thread_func)
# t1.start()
# t1.join()

################################################################################
# Advanced multiprocessing
################################################################################
def test_advanced_multiprocessing():
    # Process class
    pass

def just_print(x):
    print(f'Processed {x} [{multiprocessing.current_process().name}]')
    return 0

def slow_cpu_process_mp(x):
    start = time.time()
    for a in range(2 * 10**7):
        _ = a*a
    duration = time.time() - start

    p_name = multiprocessing.current_process().name
    print(f'Processed {x} in {duration:.10f}s [{p_name}]')
    
    return round(duration, 3)

def slow_io_process_mp(x):
    start = time.time()
    time.sleep(1)
    duration = time.time() - start

    p_name = multiprocessing.current_process().name
    print(f'Processed {x} in {duration:.10f}s [{p_name}]')

    return round(duration, 3)

def test_multiprocessing_performance_gain():
    '''
    The performance gain you can expect from multiprocessing is less than what
    you naively expect from splitting something to run in parallel. The
    following factors lower performance gains overall and per process:
        1) Setup overhead for each process
        2) Other programs utilizing the CPU cores. 
    '''
    inputs = list(range(multiprocessing.cpu_count()))

    ############################################################################
    print('Time overhead from setting up processes')
    start = time.time()
    with multiprocessing.Pool() as pool:
        _ = pool.map(just_print, inputs)
    duration = round(time.time() - start, 3)
    print(f'Setup Overhead: {duration}s\n')

    ############################################################################
    print('Running slow CPU processes with single process')
    start = time.time()
    time_per_input = [slow_cpu_process_mp(x) for x in inputs]
    duration = round(time.time() - start, 3)
    print(f'Total Time: {duration}s\n')

    print('Running slow CPU processes with multiprocessing')
    for n_cores in  range(1, multiprocessing.cpu_count()+1):
        print(f'Running with {n_cores} cores')
        start = time.time()
        with multiprocessing.Pool(n_cores) as pool:
            time_per_input_mp = pool.map(slow_cpu_process_mp, inputs)
        duration = round(time.time() - start, 3)
        print(f'Total Time: {duration}s\n')
    
    # Time per process will be worse as more processes are spawned. Perhaps this
    # is because for the single process approach, the OS can allow that one
    # process to have full utilization of the core while for the multiprocessing
    # approach this is not possible. The program is requesting to use all 4
    # cores and so the OS is more likely to interrupt these to run other things. 
    # See: "Speed per process getting slower with more processes"
    # https://stackoverflow.com/questions/66828008/
    assert mean(time_per_input) < mean(time_per_input_mp)

    print('Running slow IO processes with a single process')
    start = time.time()
    time_per_input = [slow_io_process_mp(x) for x in inputs]
    duration = round(time.time() - start, 3)
    print(f'Total Time: {duration}s\n')

    print('Running slow IO processes with multiprocessing')
    for n_cores in  range(1, multiprocessing.cpu_count()+1):
        print(f'Running with {n_cores} cores')
        start = time.time()
        with multiprocessing.Pool(n_cores) as pool:
            time_per_input_mp = pool.map(slow_io_process_mp, inputs)
        duration = round(time.time() - start, 3)
        print(f'Total Time: {duration}s\n')

    # Time per process will be much closer than when running slow CPU process
    avg_time_1p = mean(time_per_input)
    avg_time_mp = mean(time_per_input_mp)
    avg_time = (avg_time_1p + avg_time_mp) / 2
    diff = abs(avg_time - avg_time_mp)
    diff_perc = diff / avg_time
    print(f'{diff_perc:.3%} diff in time per process '
           'between single and multiprocess for IO bound processes')
    
def main():
    # inputs = list(range(n_inputs))
    # print(f'Input: {inputs}')

    #print('\nSynchronous tasking')
    #start = time.time()
    #result1 = simple_synchronous_tasking(inputs)
    #duration = time.time() - start
    #print(f'Processed {n_inputs} inputs sequentially in {duration:.3f} seconds')
    #print(f'Result = {result1}')
    #
    #print('\nPre-emptive multi-tasking')
    #start = time.time()
    #result2 = simple_preemptive_multitasking(inputs, max_threads)
    #duration = time.time() - start
    #print(f'Processed {n_inputs} inputs on {max_threads} threads in {duration:.3f} seconds')
    #print(f'Result = {result2}')

    #print('\nCooperative multi-tasking')
    #start = time.time()
    #result3 = simple_cooperative_multitasking(inputs, max_threads)
    #duration = time.time() - start
    #print(f'Processed {n_inputs} inputs on {max_threads} threads in {duration:.3f} seconds')
    #print(f'Result = {result3}')

    # print('\nAdvanced asyncio')
    # Coroutines are run at the top level (i.e. not within a coroutine function) using run()
    # The run command can be nested as deeply as one wants within normal functions though
    #asyncio.run(advanced_cooperative_multitasking())
    #asyncio.run(test_read_and_write())

    ## CPU Bound
    start = time.time()
    print('\nSynchronous processing')
    simple_synchronous_processing()
    duration = time.time() - start
    print(f'Ran {n_processes} processes in {duration:.3f} seconds')
    
    start = time.time()
    print('\nMultiprocessing')
    simple_multiprocessing()
    duration = time.time() - start
    print(f'Ran {n_processes} processes in {duration:.3f} seconds')

    #print('\nDemo of multiprocessing performance gains')
    #test_multiprocessing_performance_gain()

    #example_race_condition()

if __name__ == '__main__':
    main()
