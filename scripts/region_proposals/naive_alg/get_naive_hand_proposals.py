"""
Description
-----------
Computes and saves naieve hand proposals from hand detections.

Usage
-----
```
python get_naieve_hand_proposals.py <det dir> <out dir>
```

Example
-------
```
python get_naive_hand_proposals.py \
/home/vj/Dropbox/steeparthi/HARP-root/data/hands/detection/testing/mmaction2/faster-rcnn/C1L1P-C/20170330 \
/home/vj/Dropbox/steeparthi/HARP-root/data/hands/proposals/naive/C1L1P-C/20170330
```
"""
import pdb
import argparse
from argparse import RawTextHelpFormatter
from harp.region_proposals.naive_alg import NaiveAlg
from harp import fdops


description = ("""
Description
-----------
Computes and saves naive hand proposals from hand detection.
""")


def _arguments():
    """Parses input arguments."""

    # Initialize arguments instance
    args_inst = argparse.ArgumentParser(description=(description),
                                        formatter_class=RawTextHelpFormatter)

    # Adding arguments
    args_inst.add_argument(
        "det_dir",
        type=str,
        help=("directory having csv files with bounding boxes.")
    )
    args_inst.add_argument(
        "out_dir",
        type=str,
        help=("Output directory location")
    )
    args = args_inst.parse_args()

    # Crates a dictionary having arguments and their values
    args_dict = {'det_dir': args.det_dir, 'out_dir': args.out_dir}

    # Return arguments as dictionary
    # Hello world how are you doing
    return args_dict


def main():
    """Main function."""

    # Input arguments
    argd = _arguments()
    det_dir = argd['det_dir']
    out_dir = argd['out_dir']

    # All csv files in current directory
    fdops.check_if_dir_exists(det_dir)
    csv_list = fdops.get_files_with_kws(det_dir, ["30fps", "det_per_sec.csv"])

    # loop through all the csv files
    for det_csv in csv_list:
        print(f"USER_INFO: Processing \n\t{det_csv}")

        # Initialize naive algorithm instance
        naive_alg = NaiveAlg(det_csv, naive_interval=3)

        # Write a csv file having proposals
        naive_alg.to_csv(out_dir)


# Execution starts here
if __name__ == "__main__":
    main()
