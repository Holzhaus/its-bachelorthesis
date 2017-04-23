# -*- coding: utf-8 -*-
import multiprocessing
import queue
import logging
import resource
import signal
import subprocess
import os


class WorkerProcess(multiprocessing.Process):
    def __init__(self, target):
        super().__init__()
        self.daemon = True
        self._output_queue = multiprocessing.Queue()
        self.max_secs = 10
        self.max_cpu_secs = 10
        self.max_vmem_size = 750*1024**2  # 300 MiB should suffice
        self.target = target

    def run(self):
        logger = multiprocessing.log_to_stderr()
        logger.setLevel(logging.DEBUG)

        resource.setrlimit(resource.RLIMIT_CPU, (self.max_cpu_secs,)*2)
        logger.info('RLIMIT_CPU = %d seconds', self.max_cpu_secs)
        resource.setrlimit(resource.RLIMIT_AS, (self.max_vmem_size,)*2)
        logger.info('RLIMIT_RSS set to %d bytes', self.max_vmem_size)
        rusage = resource.getrusage(resource.RUSAGE_SELF)
        logger.info('Memory info: %r', rusage)
        logger.info('Page size: %d', resource.getpagesize())
        logger.info('Maximum Resident Set Size: %d * %d = %d',
                    rusage.ru_maxrss, resource.getpagesize(),
                    rusage.ru_maxrss*resource.getpagesize())

        try:
            result = self.target()
        except subprocess.CalledProcessError as e:
            result = None
            if e.returncode < 0:
                logger.info('Child process died, committing suicide using ' +
                            'signal %s (%d).',
                            signal.Signals(-e.returncode).name, -e.returncode)
                os.kill(os.getpid(), -e.returncode)
                signal.pause()

        self._output_queue.put_nowait(result)
        logger.info('Maximum Resident Set Size: %r',
                    rusage.ru_maxrss*resource.getpagesize())

    def get_result(self):
        try:
            retval = self._output_queue.get_nowait()
        except queue.Empty:
            retval = None
        exitcode = self.exitcode
        return (exitcode, retval)

    def execute(self, timeout=None):
        logger = logging.getLogger(__name__)
        self.start()
        logger.info('PID of spawned process: %d', self.pid)
        self.join(timeout)
        if self.is_alive():
            self.terminate()
            self.join()
        return self.get_result()
