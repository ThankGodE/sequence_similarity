"""list of functions that handle files"""
import csv
import glob
import os


# functions, class and methods
def globally_get_all_files(path2directory: str, file_extension=None) -> list:
    """gets all files in a directory if supplied with a path to all files
    e.g. (/path/to/file, 'fasta')"""

    if file_extension is None:
        all_files = glob.glob(path2directory + os.sep + "*")

    elif file_extension is not None:
        all_files = glob.glob(
            path2directory + os.sep + "**" + os.sep + "*" + file_extension,
            recursive=True,
            )

    return __decode_bom(all_files)


def read_csv(csv_file: str, delimiter: str) -> list[str]:
    """ get csv contents as Generators """

    with open(csv_file, 'r') as csv_file_content:

        return list(csv.reader(csv_file_content, delimiter=delimiter))


def __decode_bom(all_path2file: list) -> list:
    """ decodes BOM i string """

    all_files_bom_decoded = [
        file.encode().decode("utf-8-sig") for file in all_path2file
    ]

    return all_files_bom_decoded