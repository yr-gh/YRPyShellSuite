# -*- coding: utf-8 -*-
"""
Basic utilities.

@author: Rui Yang
"""


import os
import sys
import logging
import subprocess
import time


# Configuring log module
logging.basicConfig(
    format = '[%(asctime)s | %(process)d-%(thread)d | %(levelname)s] %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S',
    level = logging.INFO, stream = sys.stdout)
log = logging.getLogger(__name__)


def run_shell_cmd(cmd, shell_path = None, force_exit = False):
    """Running shell commands.
    
    `cmd` must be a single string."""
    log.info('CMD={}\n'.format(cmd))
    
    final_cmd = []
    if shell_path:
        final_cmd.append(shell_path)
    else:
        final_cmd.append('/usr/bin/bash')
    final_cmd.append('-c')
    final_cmd.append(cmd)
    
    log.info('FINAL_CMD={}\n'.format(final_cmd))
    
    t0 = time.perf_counter()
    p = subprocess.run(
        final_cmd,
        shell = False, check = False,
        stdout = subprocess.PIPE, stderr = subprocess.PIPE,
        universal_newlines = True)
    t1 = time.perf_counter()
    
    rc = p.returncode
    stderr = p.stderr.strip()
    stdout = p.stdout.strip()
    durtime = (t1-t0) / 60.0
    return_str = 'RC={rc} DURATION_MIN={dur:.1f}\nSTDERR={err}\nSTDOUT={out}\n'.format(
        rc = rc,
        dur =  durtime,
        err = stderr,
        out = stdout)
    
    if force_exit and rc:
        log.error(return_str)
        log.error('The program has non-zero exit status, exiting ...')
        exit(1)
    elif rc:
        log.error(return_str)
    
    return [rc, stderr, stdout, durtime]

def valid_files(files):
    """Check whether all files are valid.
    
    `files` is an iterable object."""
    if len(files) > 0 and all(tuple(map(lambda x: os.path.isfile(x), files))):
        return True
    else:
        return False

def valid_dirs(dirs):
    """Check whether all directories are valid.
    
    `dirs` is an iterable object."""
    if len(dirs) > 0 and all(tuple(map(lambda x: os.path.isdir(x), dirs))):
        return True
    else:
        return False

def mkdir_p(x):
    """Create the path recursively.
    
    If the path has already existed, print a warning, then return False, or return True."""
    try:
        os.makedirs(x, exist_ok = False)
    except FileExistsError:
        log.warning('{} has already existed!'.format(x))
        return False
    else:
        return True
