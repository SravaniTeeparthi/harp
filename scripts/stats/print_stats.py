import pdb
import pandas as pd
import cv2
import argparse
from harp import fdops
import numpy as np


def _arguments():
    """ Parses input arguments """

    # Initialize arguments instance
    args_inst = argparse.ArgumentParser(description=(
        "Prints activity label summary to standard console"))
    args_inst.add_argument("rdir",
                           type=str,
                           help=("root directory having activity labels"))
    args_inst.add_argument("labels_fname",
                           type=str,
                           help=("Activity labels file name (csv)"))

    # Parse arguments
    args = args_inst.parse_args()

    # Crate a dictionary having arguments and their values
    args_dict = {'rdir': args.rdir, 'labels_fname': args.labels_fname}

    # Return arguments as dictionary
    return args_dict


# Execution starts here
if __name__ == "__main__":
    args = _arguments()

    # Creating ActivityLabels instance
    act_labels = fdops.get_files_with_kws(args['rdir'], args['labels_fname'])
    df = fdops.load_all_activity_labels(act_labels)
    print("Median value of width :" ,np.median(df['w']))
    print("Median value of height :" ,np.median(df['h']))
    pdb.set_trace()
