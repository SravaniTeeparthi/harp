"""
Description
-----------
Creates a csv file with naive writing/typing region proposals (base line) using
hand detections.

The output CSV file has proposals for every three seconds. The file is saved
in the same directory with name, "<video_name>_props.csv"

Example
-------
```
python baseline_region_proposals <root dir>
```

Note
----
+ It is assumed that the root directory has csv files containing following
  columns, `f0   W   H   FPS w0  h0  w   h`.
"""
import glob
import os
import argparse
import pandas as pd


def _arguments():
    """Parses input arguments."""

    # Initialize arguments instance
    args_inst = argparse.ArgumentParser(
        description=("""Creates a csv file with naive writing/typing region
                        proposals (base line) using hand detections."""))

    # Adding arguments
    args_inst.add_argument(
            "rdir",
            type=str,
            help=("Root directory having hand detection csv files."))
    args = args_inst.parse_args()

    # Crate a dictionary having arguments and their values
    args_dict = {'rdir': args.rdir}

    # Return arguments as dictionary
    # Hello world how are you doing
    return args_dict


def main():
    """Main function."""
    argd = _arguments()
    rdir = argd['rdir']

    # Check if the the directory exist
    if not os.path.isdir(rdir):
        raise Exception(f"U-ERROR: {rdir} does not exist.")

    # Get all the csv files in the directory
    csvs = glob.glob(rdir+"/*.csv")

    # CSV file loop
    for csv in csvs:
        cdf = pd.read_csv(csv)
        import pdb; pdb.set_trace()
        sframe = cdf['f0'].max



# Execution starts here
if __name__ == "__main__":
    main()
