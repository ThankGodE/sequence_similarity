"""
A collection of functions that performs file writing operations.
"""

__name__ = "__main__"

import logging
import pandas as pd


from package.enumsoperations.delimiter_enums import Delimiters


class FileWriter:
    """ The FileWriter class handles the writing of the data to a file. """

    file_path: str = None
    mode: str = None

    def __init__(self, file_path, mode):
        """
        Creates a new FileWriter object.

        :param file_path: Path to the file.
        :param mode: Mode of the file.
        """
        self.file_path = file_path
        self.mode = mode

    def write_filtered_reads(self, filtered_reads: object()):
        """ Write filtered out reads containing generator object to file """

        with open(self.file_path, self.mode) as filtered_out_content:

            for filtered_read in filtered_reads:

                filtered_read_bed = Delimiters.TAB_SEPERATOR.join(filtered_read)

                filtered_out_content.write(filtered_read_bed + Delimiters.NEW_LINER)

        logging.info("Filtered reads written to file:  {}".format(self.file_path))

    def write_str(self, data: str) -> None:
        """
        Writes data to a file. Data here is a string

        :param data: String data to write.
        """

        with open(self.file_path, self.mode) as file:
            file.write(data)

        logging.info("writing data to {}".format(self.file_path))

    def write_df(self, data: pd.DataFrame, delimiter: str, header: bool) -> None:
        """
        Writes data to a file. Data here is a DataFrame. To show progress bar add progress=True to data.export()

        :param data: DataFrame to write.
        :param delimiter: Delimiter to use.
        :param header: Write header or not.
        """

        data.to_csv(self.file_path, sep=delimiter, header=header, index=False)

        logging.info(" writing dataframe to file: {}".format(self.file_path))