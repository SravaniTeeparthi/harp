"""
Description
-----------
For every second of video, check if there are any writing instances.
If atleast 50% of the frames have writing then save the instance to csv file.

for all the writing Instances, get hands from the frames and calculate
IoU ratios of each detection with wriitng ground truth. Take the max IoU
ratio and save the csv file.
Classify as succes or failure
Example
-------
```
python get_performance.py
C:/Users/vj/Dropbox/writing-nowriting-GT/C1L1P-C/20170330/gTruth-wnw_30fps.csv
C:/Users/vj/Dropbox/typing-notyping/C1L1P-C/20170330/properties_session.csv
C:/Users/vj/Dropbox/steeparthi/HARP-root/software/sravani-git/harp@sravani/scripts/alg_1/performance_csvs/G-C1L1P-Mar30-C-Kelly_q2_01-06_30fps.csv
C:/Users/vj/Dropbox/steeparthi/HARP-root/results/performance/alg1/
```
"""
import os
import argparse
import pandas as pd
import pdb
from harp.region_proposals.performance import Performance
from harp import fdops

def _arguments():
    """Parses input arguments."""

    # Initialize arguments instance
    args_inst = argparse.ArgumentParser(
        description=("""

            """))

    # Adding arguments
    args_inst.add_argument("gt_csv",
        type=str,
        help=("Ground Truth csv"))

    args_inst.add_argument("vid_property_csv",
        type=str,
        help=("CSV file having video properties."))

    args_inst.add_argument("method_csv",
        type=str,
        help=("Method csv with which the gt file should be compared "))

    args_inst.add_argument("out_pth",
        type=str,
        help=("Path to save perforamnce csv "))

    args = args_inst.parse_args()

    # Crate a dictionary having arguments and their values
    args_dict = {'gt_csv': args.gt_csv, 'vid_property_csv': args.vid_property_csv , 'm_csv': args.method_csv, 'out_pth': args.out_pth}

    # Return arguments as dictionary
    return args_dict


def main():
    """Main function."""
    argd = _arguments()
    print(argd)

    # read csv files
    gt_csv      = argd['gt_csv']
    prop_csv    = argd['vid_property_csv']
    m_csv       = argd['m_csv']
    out_pth     = argd['out_pth']

    # Cgeck if file/dir exists
    fdops.check_if_file_exists(gt_csv)
    fdops.check_if_file_exists(prop_csv)
    fdops.check_if_file_exists(m_csv)
    fdops.check_if_dir_exists(out_pth)

    # Creating class Instance
    perf             =   Performance(gt_csv,prop_csv,m_csv,out_pth)
    p_gtrows         =   perf.get_video_df_from_gt()
    p_gt_df          =   pd.DataFrame(p_gtrows, columns=["vid_name","f0","f1","kid","w0","h0","w","h"])
    pf_final_rows    =   perf.cal_iou(p_gt_df)
    perf.to_csv(pf_final_rows)

# Execution starts here
if __name__ == "__main__":
    main()
