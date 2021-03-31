"""
Description
-----------
Computes and saves proposal regions from projections as csv

Usage
-----
```
python get_alg1_region_proposal.py <projections dir> <session properties csv > <out dir>
```

Example
-------
```
python get_alg1_region_proposal.py \
C:/Users/vj/Dropbox/steeparthi/HARP-root//data/hands/detection/testing/mmaction2/faster-rcnn/C1L1P-C/20170330/G-C1L1P-Mar30-C-Kelly_q2_01-06_30fps_det_per_sec/ \
C:\Users\vj\Dropbox\typing-notyping\C1L1P-C\20170330/properties_session.csv C:\Users\vj\Dropbox\steeparthi\HARP-root\data\hands\proposals\alg1\C1L1P-C\20170330\1_det_per_sec/
```
"""


import cv2
import pdb
import numpy as np
import os
import pandas as pd
from natsort import os_sorted
from harp.region_proposals.alg_1 import Alg1
from argparse import RawTextHelpFormatter
import argparse
from harp import fdops


description = ("""
Description
-----------
Computes and saves proposal regions from projections as csv
""")


def _arguments():
    """Parses input arguments."""

    # Initialize arguments instance
    args_inst = argparse.ArgumentParser(description=(description),
                                        formatter_class=RawTextHelpFormatter)

    # Adding arguments
    args_inst.add_argument(
        "proj_path",
        type=str,
        help=("Directory having projections for each session")
    )
    args_inst.add_argument(
        "properties_csv",
        type=str,
        help=("Csv file for session properties")
    )
    args_inst.add_argument(
        "out_pth",
        type=str,
        help=("Output path for csv file")
    )
    args = args_inst.parse_args()

    # Crates a dictionary having arguments and their values
    args_dict = {'proj_path': args.proj_path, 'properties_csv': args.properties_csv , 'out_pth': args.out_pth}

    # Return arguments as dictionary
    return args_dict




def main():
    """Main function."""

    # Input arguments
    argd = _arguments()
    proj_path       = argd['proj_path']
    properties_csv  = argd['properties_csv']
    out_pth         = argd['out_pth']

    # Check if directory exists
    fdops.check_if_dir_exists(proj_path)
    files = os_sorted(os.listdir(proj_path))
    c_rows = []
    for f in files :
        img_pth         = os.path.join(proj_path,f)
        alg1            = Alg1(img_pth, properties_csv, out_pth)
        each_row        = alg1.proj_to_proposal()
        c_rows = c_rows + [each_row]
    c_rows          = alg1.proposals_to_csv(c_rows)



# Execution starts here
if __name__ == "__main__":
    main()
