import time
import multiprocessing
from statistics import mean

def just_print(x):
    print(f'Processed {x} [{multiprocessing.current_process().name}]')
    return 0

def slow_cpu_process(x):
    start = time.time()
    for a in range(2 * 10**7):
        _ = a*a
    duration = time.time() - start

    p_name = multiprocessing.current_process().name
    print(f'Processed {x} in {duration:.10f}s [{p_name}]')
    
    return round(duration, 3)

def slow_io_process(x):
    start = time.time()
    time.sleep(1)
    duration = time.time() - start

    p_name = multiprocessing.current_process().name
    print(f'Processed {x} in {duration:.10f}s [{p_name}]')

    return round(duration, 3)

def main():
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
    time_per_input = [slow_cpu_process(x) for x in inputs]
    duration = round(time.time() - start, 3)
    print(f'Total Time: {duration}s\n')

    print('Running slow CPU processes with multiprocessing')
    for n_cores in  range(1, multiprocessing.cpu_count()+1):
        print(f'Running with {n_cores} cores')
        start = time.time()
        with multiprocessing.Pool(n_cores) as pool:
            time_per_input_mp = pool.map(slow_cpu_process, inputs)
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
    time_per_input = [slow_io_process(x) for x in inputs]
    duration = round(time.time() - start, 3)
    print(f'Total Time: {duration}s\n')

    print('Running slow IO processes with multiprocessing')
    for n_cores in  range(1, multiprocessing.cpu_count()+1):
        print(f'Running with {n_cores} cores')
        start = time.time()
        with multiprocessing.Pool(n_cores) as pool:
            time_per_input_mp = pool.map(slow_io_process, inputs)
        duration = round(time.time() - start, 3)
        print(f'Total Time: {duration}s\n')

    # This will be much closer than when running slow CPU process
    avg_time_1p = mean(time_per_input)
    avg_time_mp = mean(time_per_input_mp)
    avg_time = (avg_time_1p + avg_time_mp) / 2
    diff = abs(avg_time - avg_time_mp)
    diff_perc = diff / avg_time
    print(f'{diff_perc:.3%} diff in time per process '
           'between single and multiprocess for IO bound processes')


if __name__ == '__main__':
    main()