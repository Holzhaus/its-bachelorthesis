# -*- coding: utf-8 -*-
import multiprocessing
import queue
import logging
import resource
import signal
import subprocess
import os


def work(target, ctx, output_queue, max_cpu_secs, max_vmem_size):
    logger = ctx.log_to_stderr()
    logger.setLevel(logging.DEBUG)

    if max_cpu_secs:
        resource.setrlimit(resource.RLIMIT_CPU, (max_cpu_secs,)*2)
        logger.info('RLIMIT_CPU = %d seconds', max_cpu_secs)

    if max_vmem_size:
        resource.setrlimit(resource.RLIMIT_AS, (max_vmem_size,)*2)
        logger.info('RLIMIT_RSS set to %d bytes', max_vmem_size)

    rusage = resource.getrusage(resource.RUSAGE_SELF)
    logger.info('Memory info: %r', rusage)
    logger.info('Page size: %d', resource.getpagesize())
    logger.info('Maximum Resident Set Size: %d * %d = %d',
                rusage.ru_maxrss, resource.getpagesize(),
                rusage.ru_maxrss*resource.getpagesize())

    try:
        result = target()
    except subprocess.CalledProcessError as e:
        result = None
        if e.returncode < 0:
            logger.info('Child process died, committing suicide using ' +
                        'signal %s (%d).',
                        signal.Signals(-e.returncode).name, -e.returncode)
            os.kill(os.getpid(), -e.returncode)
            signal.pause()
    except (OSError, MemoryError):
            sgn = signal.SIGSEGV
            logger.info('Child process ran out of memory, committing suicide' +
                        ' using signal %s (%d).',
                        sgn.name, sgn)
            os.kill(os.getpid(), sgn)
            signal.pause()
    output_queue.put_nowait(result)
    logger.info('Maximum Resident Set Size: %r',
                rusage.ru_maxrss*resource.getpagesize())


def execute(target, ctx=None, timeout=30):
    logger = logging.getLogger(__name__)

    max_cpu_secs = 10
    max_vmem_size = 750*1024**2  # 300 MiB should suffice

    if not ctx:
        logger.debug('No multiprocessing context given, using default one...')
        ctx = multiprocessing.get_context()

    output_queue = ctx.Queue()
    process = ctx.Process(target=work, args=(target, ctx, output_queue, max_cpu_secs, max_vmem_size))
    process.daemon = True
    process.start()

    logger.info('PID of spawned process: %d', process.pid)
    process.join(timeout)
    if process.is_alive():
        process.terminate()
        process.join()
    logger.info('Process terminated.')

    try:
        retval = output_queue.get_nowait()
    except queue.Empty:
        retval = None
    exitcode = process.exitcode
    return (exitcode, retval)
