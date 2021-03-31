"""
The following module contains functions that help in file and directory
operations.
"""
import os
import pdb
import glob
import pathlib
import warnings
import pandas as pd

def check_if_file_exists(file_path):
    """
    If file does not exists it raises an exception

    Parameters
    ----------
    file_path : str
        Full path to file
    """
    if not os.path.isfile(file_path):
        raise Exception(f"The file does not exist,\n\t{file_path}")

def check_if_dir_exists(directory_path):
    """
    If file does not exists it raises an exception

    Parameters
    ----------
    directory_path : str
        Full path of directory
    """
    if not os.path.isdir(directory_path):
        raise Exception(f"The directory does not exist,\n\t{directory_path}")


def get_file_list(loc, ext):
    """ The following function returns all the files ina directory
    having an extension. This does not do recursive search.

    Parameters
    ----------
    loc : str
        File location
    ext : str
        File extension
    """
    return glob.glob(f"{loc}/*.{ext}")

def get_files_with_kws(loc, kws):
    """
    Lists full paths of files having certian keywords in their names

    Parameters
    ----------

    loc : str
    Path to the root directory containing files.
    kws : list of str
    List of key words the files have
    """
    # Check if directory is valid
    if not (os.path.exists(loc)):
        raise Exception(f"The path {loc} is not valid.")

    # create a list using comma separated values
    kw_lst_csv = []
    for idx, litem in enumerate(kws):
        litem_split = litem.split(",")
        if len(litem_split) > 1:
            kw_lst_csv = kw_lst_csv + litem_split
        else:
            kw_lst_csv.append(litem_split[0])

    # Loop through each file
    files = []
    for r, d, f in os.walk(loc):
        for file in f:
            # Break comma separated values
            # Check if current file contains all of the key words
            is_valid_file = all(kw in file for kw in kw_lst_csv)
            if is_valid_file:
                files.append(os.path.join(r, file))

    # return
    return files


def get_file_list_recursive(loc, ext):
    """ The following function returns all the files ina directory
    having an extension. This does not do recursive search.

    Parameters
    ----------
    loc : str
        File location
    ext : str
        File extension
    """
    return glob.glob(f"{loc}/**/*.{ext}", recursive=True)


def get_loc_name_ext(full_path):
    """
    Given a full path this function will returns a tuple having
    following information,
    full directory path, file name, file extension
    """
    check_if_file_exists(full_path)

    file_loc = os.path.dirname(full_path)
    fname_with_ext = os.path.basename(full_path)
    fname, ext = os.path.splitext(fname_with_ext)

    ext = ext[1:]
    file_loc = os.path.abspath(file_loc)

    return file_loc, fname, ext


def recursive_mkdir(dir_path):
    """ Create directory recursively.
    """
    if not os.path.isdir(dir_path):
        path = pathlib.Path(dir_path)
        path.mkdir(parents=True)
        print(f"USER_INFO: Creating directory\n\t{dir_path}")

def load_all_activity_labels( flist):
    """ Loads all activity labels into one dataframe.

    Parameters
    ----------
    flist: list of str
        List of csv file paths having activity labels.
    """
    dflst = []
    for f in flist:
        dflst += [pd.read_csv(f)]

    return pd.concat(dflst, ignore_index=True)
