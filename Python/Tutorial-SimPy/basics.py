
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import simpy

def process_summary_str(p: simpy.Process) -> str:
    if p is None:
        return "None"
    d = {
        # Attributes
        'is_alive'  : p.is_alive,
        'triggered' : p.triggered,
        'processed' : p.processed,
        'ok'        : p.ok    if p.triggered else None,
        'value'     : p.value if p.triggered else None,
        'defused'   : p.defused,
        # References
        'target'    : event_summary_str(p.target),
        'callbacks' : p.callbacks,
        'env'       : p.env,
    }
[
 'callbacks',
 'defused',
 'env',
 'triggered',
 'fail',
 'ok',
 'processed',
 'succeed',
 'trigger',
 'value'
    # Methods
    # p.fail()
    # p.succeed()
    # p.trigger()
    # p.interrupt()

    return str(d)

def event_summary_str(e: simpy.Event) -> str:
    if e is None:
        return None
    d = {
        # Attributes
        'is_alive'  : p.is_alive,
        'triggered' : p.triggered,
        'processed' : p.processed,
        'ok'        : p.ok    if p.triggered else None,
        'value'     : p.value if p.triggered else None,
        'defused'   : p.defused,
        # References
        'target'    : event_summary_str(p.target),
        'callbacks' : p.callbacks,
        'env'       : p.env,
    }
    return str(d)
    
env = simpy.Environment()

def my_process(env: simpy.Environment, pid: int, time: int):
    print(f'{pid} - {env.now}) Running Process:\n\t', process_summary_str(env.active_process))
    # Creatpe timeout event that will complete 10 steps from now
    event = env.timeout(time)
    # Yield event back to environment, which will 
    yield event
    print(f'{pid} - {env.now}) Entering back into process:\n\t', process_summary_str(env.active_process))

p1 = env.process(my_process(env, 1, 10))
p2 = env.process(my_process(env, 2, 5))

print(f'1 - {env.now}) Process processed:\n\t', process_summary_str(p1))
print(f'2 - {env.now}) Process processed:\n\t', process_summary_str(p2))

# env.run()
# print(f'1 - {env.now}) Process Done:\n\t', process_summary_str(p1))
# print(f'2 - {env.now}) Process Done:\n\t', process_summary_str(p2))
# print('DONE:', env.now)