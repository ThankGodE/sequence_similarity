"""
A collection of functions that performs profiling logging tasks within a script.

"""

__name__ = "__main__"

# system modules, packages, libraries, and programs ###
import os
import sys
import time
import logging
import resource
import psutil


class ProfileLogger:
    """ logs profiling runs """

    def __init__(self, profile_began: tuple, profile_end: float) -> None:
        self.profile_start = profile_began
        self.profile_terminate = profile_end

    def log_profiling(self) -> None:
        """ logs memory and time associated with script """
        profile_commence = self.profile_start
        profile_discontinue = self.profile_terminate
        time_start = profile_commence[0]
        memory_in_mb = profile_commence[1]
        time_end = profile_discontinue

        logging.debug("\n")
        logging.debug(
            " Calculated time used by time() in minutes: {}".format(
                str((time_end - time_start) / 60)
            )
        )
        logging.debug(" Memory usage by resource (Mb): {}".format(str(memory_in_mb)))
        logging.debug(" Memory usage by psutil (Mb): {}".format(print_mem()))

        # logs script activities ###
        logging.debug(" Name of script run: {}".format(sys.argv[0].split("/")[-1]))
        logging.debug(" Absolute script path: {}".format(os.path.abspath(sys.argv[0])))
        logging.debug(
            " Commandline arguments run: {}".format(" ".join(map(str, sys.argv)))
        )
        logging.debug(" Folder where script was run: {}".format(os.getcwd()))


def begin_profiling(path_to_file: str) -> tuple:
    """logs program processes, logs start run time,checks memory using
    resource in kilobytes divided by 1000 for memory usage in Mb"""

    print("\npath to profiling records: {}\n".format(path_to_file))

    logging.basicConfig(
        filename=path_to_file,
        level=logging.DEBUG,
        format="%(asctime)s:%(levelname)s:%(message)s",
    )

    time_start = time.time()

    resource_object = resource.getrusage(resource.RUSAGE_SELF)
    memory_in_mb = resource_object.ru_maxrss / 1000

    profiled_mem_time = (time_start, memory_in_mb)

    return profiled_mem_time


def end_profiling() -> float:
    """ logs end run time """
    time_end = time.time()

    return time_end


def print_mem() -> str:
    """
    determine memory usage.
    mem = divides by 1k to get the measurement in kilobytes (rather than bytes).
    mem = divides by 1k again to get the measurement in megabytes
    (rather than kilobytes as per first mem above)
    """
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / 1000
    mem = mem / 1000

    return str(mem)
