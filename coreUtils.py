# -*- coding: utf-8 -*-
"""
Core utilities.

@author: Rui Yang
"""


import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from YRPyShellSuite.baseUtils import log, valid_files, valid_dirs


def par_thread(iterable, func, /, return_type = 'list', max_workers = None, thread_name_prefix = '', timeout = None, check_files = False, check_dirs = False, **kwargs):
    """Parallelizing tasks by multi-threading.
    
    `iterable` is an iterable object.
    
    `return_type` can be either a list ('list') or a dictionary ('dict').
    
    If `return_type` is a dictionary, the elements of the `iterable` will be used as the keys of the returned dictionary.
    
    In this situation, the elements of the `iterable` should be different from each other, and be valid keys of a dictionary object.
    
    The number of threads equal to the `len(iterable)` will be created.
    
    But at most `max_workers` will be executed concurrently.
    
    `check_files` and `check_dirs` will only work when `itereable` is a string iterable object, 
    containing file or directory pathes.
    
    All keyword arguments packed in `kwargs` will be passed to `func`.
    
    In brief, your function `func` will only be allowed to accept one position argument (one element in `iterable`), 
    and a number of kweyword arguments packed by `**kwargs`"""
    if check_files == True and check_dirs == True:
        log.error('Only either `check_files` or `check_dirs` can be True! Program will exit ...')
        exit(1)
    
    if check_files and valid_files(iterable):
        log.info('All files exist!')
    elif check_files and not valid_files(iterable):
        log.error('Not all files exist! Program will exit ...')
        exit(1)
    
    if check_dirs and valid_dirs(iterable):
        log.info('All directories exist!')
    elif check_dirs and not valid_dirs(iterable):
        log.error('Not all directories exist! Program will exit ...')
        exit(1)
    
    if not max_workers:
        max_workers = min(32, os.cpu_count() + 4)
    
    if return_type == 'list':
        return_values = []
    elif return_type == 'dict':
        return_values = {x: None for x in iterable}
    else:
        log.error("Invalid return type {return_type}. Return type can only be either 'list', or 'dict'".format(return_type = return_type))
        exit(1)
    
    with ThreadPoolExecutor(max_workers = max_workers, thread_name_prefix = thread_name_prefix) as executor:
        # Load tasks
        tasks = {executor.submit(func, x, **kwargs): x for x in iterable}
        # Wait tasks to be finished
        for task in as_completed(tasks, timeout = timeout):
            x = tasks[task]
            try:
                return_data = task.result()
            except Exception as exc:
                log.error('{} generated an exception: {}'.format(x, exc))
                raise
            else:
                log.info('{} was ran successfully with return value {}!'.format(x, return_data))
                if return_type == 'list':
                    return_values.append(return_data)
                elif return_type == 'dict':
                    return_values[x] = return_data
                
    return return_values
