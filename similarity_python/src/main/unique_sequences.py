"""
This script:
    Creates a single fasta file containing all proteins from two fasta files but where each individual
    sequence in the two fast files only appears once and both IDs for that sequence included in the fasta record


Required:
    - Python >= 3.10
    - python-dotenv>=1.0.0
    - for additional dependencies, see requirements.txt
"""

# Futures local application libraries, source package
from addscriptdir2path import add_package2env_var

# re-define system path to include modules, packages
# and libraries in environment variable
add_package2env_var()

from package.profiling.profiling import begin_profiling, end_profiling, ProfileLogger
from package.commandlineoperations.commandline_input_argument_getter_unique_sequences import CliInputArgumentGetter
from package.uniquesequenceoperations.uniquesequencesoperations import UniqueSequenceOperator

profiling_starting = begin_profiling("")


###################################################
# main function                               #####
###################################################


def main() -> None:
    """main function to run commandline arguments and call other functions to run."""

    args_cli_values = CliInputArgumentGetter.get_cli_input_arguments()

    CliInputArgumentGetter.check_input_arguments(args_cli_values)

    path2output_dir = args_cli_values.path2out
    path2reference_fasta_file = args_cli_values.path2reference_fasta
    path2query_fasta_file = args_cli_values.path2query_fasta

    try:

        unique_sequence_operator: UniqueSequenceOperator = UniqueSequenceOperator(path2reference_fasta_file,
                                                                                  path2query_fasta_file,
                                                                                  path2output_dir)
        unique_sequence_operator.process_unique_sequences()

    except (ValueError, TypeError, FileNotFoundError) as e:

        if isinstance(e, ValueError):
            raise ValueError(e) from e

        if isinstance(e, TypeError):
            raise TypeError(e) from e

        if isinstance(e, FileNotFoundError):
            raise FileNotFoundError(e) from e


###################################################################################
# run __main__ ####################################################################
###################################################################################
if __name__ == "__main__":
    main()

time_end = end_profiling()
ProfileLogger(profiling_starting, time_end).log_profiling()
