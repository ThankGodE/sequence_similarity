""" append run script directory to system path """

import os
import sys
import glob
import logging

# Futures and third party libraries
from dotenv import load_dotenv


def add_package2env_var() -> None:
    """
    re-define system path to include modules, packages, and
    libraries in environment variable using dotenv
    """

    path_2_run_script_base_dir = run_script_base_dir()

    path2env_var = find_env_var_file(path_2_run_script_base_dir)

    if len(path2env_var) > 0:
        path2env_var_str = path2env_var[0]
        check_srcpkgpath_env_var(path2env_var_str)
        load_package_paths(path2env_var_str)

    elif len(path2env_var) == 0:

        env_input_status = """ .env file could not be found in current working
                        directory or parent directories"""
        logging.warning(env_input_status)
        path_to_env_var_file = input(
            "Enter absolute path to the .env environment variable file: "
        )
        load_package_paths(path_to_env_var_file)


def check_srcpkgpath_env_var(environment_variable_file: str) -> None:
    """check that the declared environment variables in the .env file exist"""

    src_package_path = [
        line.strip().split("=")[1].replace('"', "")
        for line in open(environment_variable_file).readlines()
        if line.split("=")[0] == "SOURCEPKGPATH"
    ]

    assert (
        len(src_package_path) > 0
    ), """ absolute path to src/package directory
    is not found in .env file"""

    assert os.path.exists(src_package_path[0]) and os.path.isdir(
        src_package_path[0]
    ), """ {} does not exist or is not a directory.
    update .env file:  {}   with real or existing SRCPKGPATH path and NOT this: {}""".format(
        src_package_path[0], environment_variable_file, src_package_path[0]
    )


def load_package_paths(env_var_files: str) -> None:
    """ load more than one environment variable files """

    if isinstance(env_var_files, list) is True:
        [specifically_load_files(env_file) for env_file in env_var_files]

    elif isinstance(env_var_files, str) is True:
        specifically_load_files(env_var_files)


def specifically_load_files(file2load: str) -> None:
    """ specifically load environment variable files """

    try:
        if os.path.exists(file2load) is True:
            load_dotenv(file2load, verbose=True)

    except FileNotFoundError:
        assert (
            os.path.exists(file2load) is True
        ), """ {} is not path or path does not exist""".format(file2load)

    else:
        path2package = os.getenv("SOURCEPKGPATH")
        environment_variable_file_dirname = os.path.dirname(file2load)

        sys.path.append(os.path.join(environment_variable_file_dirname, path2package))


def run_script_base_dir() -> str:
    """ get run script base directory """

    script_name = os.path.realpath(__file__)
    current_dir_name = os.path.dirname(script_name)
    parent_dir_name = os.path.split(current_dir_name)[0]

    os.environ["RUN_SCRIPT_DIR"] = parent_dir_name
    path_to_runscript_dir = os.getenv("RUN_SCRIPT_DIR")

    return path_to_runscript_dir


def find_env_var_file(path2runscript_dir: str) -> list:
    """ finds the environmental variable file"""

    last_dir = ""
    starting_dir = path2runscript_dir
    environment_var = []

    os.chdir(starting_dir)

    while last_dir != starting_dir:

        starting_dir = os.getcwd()
        env_var_file = glob.glob("*.env")

        if len(env_var_file) > 0:
            last_dir = starting_dir
            env_var_file_str = env_var_file[0]
            abs_path2env_var = os.path.join(last_dir, env_var_file_str)
            environment_var.append(abs_path2env_var)

        elif len(env_var_file) == 0:
            os.chdir("..")
            last_dir = os.getcwd()

    dir_2_put_env_file = get_dir2put_env_file()

    assert (
        len(environment_var) > 0
    ), """ a .env file was not found in any of the  parent directories.
    this .env file allows you to declare environment variables.
    please, include a .env file in the parent directory of the run script,
    /home/user/Desktop directory, phylogenetics/ directory, or here:
    {}.\n
    the later is not recommended when running test cases. you muse put it in
    the former two directories""".format(
        dir_2_put_env_file
    )

    return environment_var


def get_dir2put_env_file() -> str:
    """ get the suggested directory to put the environment variable file."""

    path2run_script = os.path.abspath(sys.argv[0])
    path2run_script_dir_name = os.path.dirname(os.path.realpath(path2run_script))

    return path2run_script_dir_name


def adddirname2syspath():
    """ adds run script directory to system path """

    script_name = sys.argv[0]

    current_dir_name = os.path.dirname(script_name)
    parent_dir_name = os.path.split(current_dir_name)[0]

    os.environ["RUN_SCRIPT_DIR"] = parent_dir_name
    path_to_runscript_dir = os.getenv("RUN_SCRIPT_DIR")
    sys.path.append(path_to_runscript_dir)
