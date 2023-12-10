"""
A collection of classes or functions that grabs commandline arguments
"""

__name__ = "__main__"

import argparse
import os
import re
import sys

from package.fileoperations.filehandlers import globally_get_all_files, read_csv
from Bio import SeqIO


class CliInputArgumentGetter:
    """Wrapper for argparse that returns an object of the class for ease of use"""

    @classmethod
    def get_cli_input_arguments(cls, args=None) -> argparse.Namespace:
        """gets input arguments from the commandline interface """

        parser = argparse.ArgumentParser(prog="process_induce_seq.py", usage="""process_induce_seq.py -h""",
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=("""
                This script:
                    Creates a single fasta file containing all proteins from two fasta files but where each individual
                    sequence in the two fast files only appears once and both IDs for that sequence included in the 
                    fasta record
                
                
                Required:
                    - Python >= 3.10
                    - python-dotenv>=1.0.0
                    - for additional dependencies, see requirements.txt

                """), )
        parser.add_argument("-o", "--path2out", help="absolute directory path to processed output files ",
                            required=True, )
        parser.add_argument("-i", "--path2reference_fasta", help="absolute path to reference assembly protein fasta "
                                                                 "file ", required=True, )

        parser.add_argument("-w", "--path2query_fasta", help="absolute path to non reference assembly protein fasta "
                                                             "file ", required=True, )

        return parser.parse_args(args)

    @classmethod
    def check_input_arguments(cls, cli_input_arguments: argparse.Namespace) -> None:
        """ check or verify input arguments """

        if not os.path.exists(cli_input_arguments.path2reference_fasta) and not os.path.isfile(
                cli_input_arguments.path2reference_fasta):
            fasta_reference_path_error_message = "path to reference proteins fasta file {} does not exist!"
            raise FileNotFoundError(fasta_reference_path_error_message.format(cli_input_arguments.path2reference_fasta))

        if not os.path.exists(cli_input_arguments.path2query_fasta) and not os.path.isfile(
                cli_input_arguments.path2query_fasta):
            fasta_query_path_error_message = "path to query proteins fasta file {} does not exist!"
            raise FileNotFoundError(fasta_query_path_error_message.format(cli_input_arguments.path2query_fasta))

        if not os.path.exists(cli_input_arguments.path2out) and os.path.isdir(cli_input_arguments.path2out):
            path_out_error_message = "output directory {} does not exist!"
            raise FileNotFoundError(path_out_error_message.format(cli_input_arguments.path2out))

        CliInputArgumentGetter.__check_fasta_files(cli_input_arguments)

    @classmethod
    def __check_fasta_files(cls, cli_input_arguments: argparse.Namespace) -> None:
        """ check if fasta files """

        all_fasta_files: list = [cli_input_arguments.path2reference_fasta, cli_input_arguments.path2query_fasta]

        for fasta_file in all_fasta_files:
            CliInputArgumentGetter.__check_fasta_file(fasta_file, "fasta file")

    @classmethod
    def __check_fasta_file(cls, fasta_file: str, file_type: str) -> None:
        """ check or verify input arguments """

        if not os.path.exists(fasta_file) and not os.path.isfile(fasta_file):
            fasta_file_path_error_message = "{} {} does not exist!"
            raise FileNotFoundError(fasta_file_path_error_message.format(file_type, fasta_file))

        try:

            for record in SeqIO.parse(fasta_file, "fasta"):

                if len(record.id) == 0:
                    raise ValueError("{} file does not contain fasta records!".format(fasta_file))

                if len(record) == 0:
                    raise ValueError("{} file does not contain records!".format(fasta_file))

                if not re.search("[A-Z]", str(record.seq.upper())):
                    raise ValueError("{} file does not contain records!".format(fasta_file))

        except ValueError as e:
            fasta_file_value_error_message = "the {} {} does not contain the right fasta data"
            raise ValueError(fasta_file_value_error_message.format(file_type, fasta_file)) from e
