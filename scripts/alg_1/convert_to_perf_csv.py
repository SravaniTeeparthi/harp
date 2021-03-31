"""This script converts the proposal csv to performance csv format
python convert_to_perf_csv.py \
C:/Users/vj/Dropbox/steeparthi/HARP-root\data\hands\proposals/alg1/C1L1P-C/20170330/1_det_per_sec/G-C1L1P-Mar30-C-Kelly_q2_01-06_30fps.csv performance_csvs/
"""


import pdb
import pandas as pd
import numpy as np
import argparse
from argparse import RawTextHelpFormatter



description = ("""
Description
-----------
This script converts the proposal csv to performance csv format
""")


def _arguments():
    """Parses input arguments."""

    # Initialize arguments instance
    args_inst = argparse.ArgumentParser(description=(description),
                                        formatter_class=RawTextHelpFormatter)

    # Adding arguments
    args_inst.add_argument(
        "csv_pth",
        type=str,
        help=("csv file path")
    )
    args_inst.add_argument(
        "out_pth",
        type=str,
        help=("Output path for csv file")
    )
    args = args_inst.parse_args()

    # Crates a dictionary having arguments and their values
    args_dict = {'csv_pth': args.csv_pth, 'out_pth': args.out_pth}

    # Return arguments as dictionary
    return args_dict

def main():
    """Main function."""

    # Input arguments
    argd = _arguments()
    csv_pth       = argd['csv_pth']
    out_pth         = argd['out_pth']
    df = pd.read_csv(csv_pth)

    f_rows= []
    for i,row in df.iterrows():
        f0 = row.f0
        f1 = row.f1
        for f in range(f0,f1,30):
            print(f0)
            n_bboxes =  row.nprops
            # pdb.set_trace()
            for l in range(0,n_bboxes):
                bbox = row.props.split(":")[l]
                xmin =  bbox.split("-")[0]
                ymin = bbox.split("-")[1]
                w = bbox.split("-")[2]
                h = bbox.split("-")[3]
                f_rows = f_rows + [[f0,"858","480","30",xmin,ymin,w,h]]
            f0 = f0+30
    f_df = pd.DataFrame(f_rows,columns=["f0","W","H","fps","w0","h0","w","h"])
    f_df.to_csv( out_pth + csv_pth.split("/")[-1],index=False)


# Execution starts here
if __name__ == "__main__":
    main()
