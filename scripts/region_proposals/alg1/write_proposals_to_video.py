"""
Description
-----------
Creates a video with proposals. The video is played at
30x, implying we mark bounding boxes for one frame per
second.

Usage
-----
```
python write_proposals_to_video.py <prop dir> <video dir> <out dir>
```

Example
-------
```
python write_proposals_to_video.py /home/vj/Dropbox/steeparthi/HARP-root/data/hands/proposals/alg1/C1L1P-C/20170330/1_det_per_sec /home/vj/Dropbox/writing-nowriting-GT/C1L1P-C/20170330 /home/vj/Dropbox/steeparthi/HARP-root/data/hands/proposals/alg1/C1L1P-C/20170330/1_det_per_sec
```
"""
import pdb
import argparse
from argparse import RawTextHelpFormatter
from harp.data_processors.proposal_data_processor import RegPropData
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
        "prop_dir",
        type=str,
        help=("Directory containing proposal csv files.")
    )
    args_inst.add_argument(
        "vid_dir",
        type=str,
        help=("Directory containing videos")
    )

    args_inst.add_argument(
        "out_dir",
        type=str,
        help=("Directory to output video.")
    )
    args = args_inst.parse_args()

    # Crates a dictionary having arguments and their values
    args_dict = {
        'prop_dir' : args.prop_dir,
        'vid_dir'  : args.vid_dir,
        'out_dir'  : args.out_dir
    }

    # Return arguments as dictionary
    # Hello world how are you doing
    return args_dict


def main():
    """Main function."""

    # Input arguments
    argd = _arguments()
    prop_dir = argd['prop_dir']
    vid_dir = argd['vid_dir']
    out_dir = argd['out_dir']

    # All csv files in current directory
    fdops.check_if_dir_exists(prop_dir)
    csv_list = fdops.get_files_with_kws(
        prop_dir,
        ["30fps_3sec_interal.csv"]
    )

    # loop through all the csv files
    for det_csv in csv_list:
        print(f"USER_INFO: Processing \n\t{det_csv}")

        # Initialize proposal data instance
        region_prop_data = RegPropData(det_csv)

        # Create video having naive region proposals
        region_prop_data.write_proposals_to_video(vid_dir, frms_per_sec=0.25)

# Execution starts here
if __name__ == "__main__":
    main()
