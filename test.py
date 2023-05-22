# -*- coding: utf-8 -*-
"""
This is only a test file for PyShellSuite.

@author: Rui Yang
"""


from YRPyShellSuite.baseUtils import run_shell_cmd
from YRPyShellSuite.coreUtils import par_thread
import time
import threading


def my_sleep(sec, kw1, kw2):
    thread = threading.current_thread()
    ThreadName = thread.name
    ThreadIdentifier = thread.ident
    ThreadNativeIdentifier = thread.native_id
    
    print('{ThreadName}-{ThreadIdentifier}-{ThreadNativeIdentifier} '
          'starting with keyword arguments kw1="{kw1}" and kw2="{kw2}" ...'.format(
              ThreadName = ThreadName,
              ThreadIdentifier = ThreadIdentifier,
              ThreadNativeIdentifier = ThreadNativeIdentifier,
              kw1 = kw1,
              kw2 = kw2))
    
    cmd = 'sleep {}'.format(sec)
    run_shell_cmd(cmd)

    print('{ThreadName}-{ThreadIdentifier}-{ThreadNativeIdentifier} '
          'done with keyword arguments kw1="{kw1}" and kw2="{kw2}"!'.format(
              ThreadName = ThreadName,
              ThreadIdentifier = ThreadIdentifier,
              ThreadNativeIdentifier = ThreadNativeIdentifier,
              kw1 = kw1,
              kw2 = kw2))
    
    return '{}-{}-{}'.format(ThreadName, ThreadIdentifier, ThreadNativeIdentifier)

if __name__ == '__main__':
    max_workers = 4
    secs = [3 for i in range(12)]
    kw1 = 'KW1 FOR TEST'
    kw2 = 'KW2 FOR TEST'
    
    print('Main thread starting ...')
    t0 = time.perf_counter()
    par_thread(secs, my_sleep, return_type = 'list', max_workers = max_workers, kw1 = kw1, kw2 = kw2)
    t1 = time.perf_counter()
    print('Main thread finished with total time cost in seconds: {}!'.format(t1 - t0))
