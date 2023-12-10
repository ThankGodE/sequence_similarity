"""
A collection of functions that performs parallelization tasks.
"""

__name__ = "__main__"

### system modules, packages, libraries, and programs ###
from pathos.serial import SerialPool


### parallelize processes using the multiprocessing function (Pickle) ###
def synchronize_processes_pathos(
        function_pathos: str, tasks2process_pathos: list, num_cpus2process_pathos: int
) -> list:
    """
    simultenously process a task
    (function, process_list, threads).
    """

    if __name__ == "__main__":

        num_processess = SerialPool(num_cpus2process_pathos)

        synchronization_output = num_processess.map(
            function_pathos, tasks2process_pathos
        )

    return synchronization_output

