"""
A collection of functions that performs unique sequence operations.
"""
import os.path
import sys

import jellyfish
import pandas as pd

from Bio import SeqIO

from package.fileoperations.filehandlers import globally_get_all_files
from package.lateralprocessing.parallelprocessing import synchronize_processes_pathos


class UniqueSequenceOperator:
    """
    A class that performs unique sequence operations. """

    reference_fasta = None
    query_fasta = None
    output_dir = None

    def __init__(self, reference_fasta: str, query_fasta: str, output_dir: str) -> None:
        """ Constructor."""

        self.reference_fasta = reference_fasta
        self.query_fasta = query_fasta
        self.output_dir = output_dir

    def process_unique_sequences(self) -> None:
        """ Processes unique sequences. """

        new_combined_records: dict = UniqueSequenceOperator.__combine_sequence_records(self)
        # UniqueSequenceOperator.__write_fasta(new_combined_records, self.output_dir)

    def __combine_sequence_records(self) -> dict:
        """ Combines sequence records. """

        reference_df: pd.DataFrame = UniqueSequenceOperator.__transform_fasta_to_dataframe(self.reference_fasta,
                                                                                           "reference_id",
                                                                                           "reference_sequence")

        query_df: pd.DataFrame = UniqueSequenceOperator.__transform_fasta_to_dataframe(self.query_fasta, "query_id",
                                                                                       "query_sequence")

        records_paired: list = [(reference_df, element) for element in query_df["query_sequence"][:20]]

        similar_records: list = synchronize_processes_pathos(process_distance,
                                                          records_paired, 8)

        similar_records_filtered: list = UniqueSequenceOperator.__remove_empty_dataframes(similar_records)
        similar_records_filtered_df: pd.DataFrame = pd.concat(similar_records_filtered).reindex()

        hundred_percent_sequence_df = pd.merge(reference_df, query_df, left_on="reference_sequence",
                                         right_on="query_sequence", how="inner")

        reference_query_ids_matched: tuple = list(zip(hundred_percent_sequence_df["reference_id"],
                                                      hundred_percent_sequence_df["query_id"]))

        reference_query_ids_matched_joined = UniqueSequenceOperator.__join_reference_query_id(
            reference_query_ids_matched)

        sequences_and_ids_matched: list = list(zip(reference_query_ids_matched_joined, hundred_percent_sequence_df[
            "reference_sequence"]))

        UniqueSequenceOperator.__write_fasta(UniqueSequenceOperator.__join_ids_with_sequences(sequences_and_ids_matched))

        pd.set_option('display.max_rows', 50)
        pd.set_option('display.width', 100)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.expand_frame_repr', False)
        print(hundred_percent_sequence_df, "EEEE")
        print(reference_query_ids_matched_joined)
        print(sequences_and_ids_matched)

    @classmethod
    def __join_ids_with_sequences(cls, reference_query_ids_matched: list) -> list:
        """ Joins the reference and query ids with the reference and query sequences."""

        return ["\n".join(element) for element in reference_query_ids_matched]



    @classmethod
    def __join_reference_query_id(cls, reference_query_ids: list) -> list:
        """ join reference and query ids """

        return [" | ".join(element) for element in reference_query_ids]

    @classmethod
    def __remove_empty_dataframes(cls, all_dataframes: list) -> list:
        """ Removes empty dataframes from the list of dataframes. """

        return [element for element in all_dataframes if len(element) > 0]

    @classmethod
    def __transform_fasta_to_dataframe(cls, fasta_file: str, id_column_name: str, sequence_column_name) -> pd.DataFrame:
        """ Transform the reference fasta file into a dataframe """

        reference_records = {}

        for ref_record in SeqIO.parse(fasta_file, "fasta"):

            if id_column_name in reference_records:
                reference_records[id_column_name].append(str(ref_record.id))

            elif id_column_name not in reference_records:
                reference_records[id_column_name] = [str(ref_record.id)]

            if sequence_column_name in reference_records:
                reference_records[sequence_column_name].append(str(ref_record.seq))

            elif sequence_column_name not in reference_records:
                reference_records[sequence_column_name] = [str(ref_record.seq)]

        return pd.DataFrame(reference_records)

    @classmethod
    def __write_fasta(cls, combined_records: list, output_dir: str) -> None:
        """ Prepares for writing. """

        path_to_output_file: str = os.path.join(output_dir, "combined_sequences.fasta")

        SeqIO.write(combined_records.values(), path_to_output_file, "fasta")

        with open(path_to_output_file, "r") as file_content:

            for element in combined_records:

                new_string = ">" + element
                file_content.write(new_string)




def process_distance(reference_df_query_sequence: tuple) -> pd.DataFrame:
    """ Takes a tuple of reference dataframe and query sequence and returns a dataframe of them"""

    reference_df, query_sequence = reference_df_query_sequence

    return check_distance_in_dataframe(reference_df, query_sequence)


def check_distance_in_dataframe(reference_df: pd.DataFrame, query_sequence: str) -> pd.DataFrame:
    """ This method checks if the distance is in the dataframe """

    process_reference_df: pd.DataFrame = reference_df.copy(deep=True)

    process_reference_df["similarity"] = process_reference_df["reference_sequence"].apply(
            is_similar_distance, query_sequence=query_sequence)

    return process_reference_df[process_reference_df["similarity"] > 0]


def is_similar_distance(reference_sequence: str, query_sequence: str) -> float:
    """ Compare the two sequences and return the number of differences """

    similarity_score: float = jellyfish.jaro_similarity(reference_sequence, query_sequence)

    if similarity_score > 0.90:
        greater_than_threshold = similarity_score

    else:
        greater_than_threshold = False

    return greater_than_threshold
