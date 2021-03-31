"""
Description
-----------
The following script converts training json log of mmdetection into
csv files. There are two csv files, capturing training and validation
logs separately.

Example
-------
```
python json_to_csvs.py <path to json file>
```
"""
import pdb
import argparse
import json
import os
import pandas as pd


def _arguments():
    """Parses input arguments."""

    # Initialize arguments instance
    args_inst = argparse.ArgumentParser(
        description=("""Script description goes here"""))

    # Adding arguments
    args_inst.add_argument("json_path", type=str, help=("JSON file path"))
    args = args_inst.parse_args()

    # Crate a dictionary having arguments and their values
    args_dict = {'json_path': args.json_path}

    # Return arguments as dictionary
    # Hello world how are you doing
    return args_dict


def main():
    """Main function."""
    argd = _arguments()

    """ Initialize training and validation dataframes """
    tdf = pd.DataFrame()
    vdf = pd.DataFrame()

    """ Load json file to a list. Each element is a line """
    with open(argd['json_path']) as f:
        content = f.readlines()
        content = [x.strip() for x in content]

    """ Loop through each line and create validation array """
    trn_list = []
    val_list = []
    for lidx, line in enumerate(content):
        line_as_dict = json.loads(line)

        if 'mode' in line_as_dict.keys():

            # Training log as list of dictionaries
            if line_as_dict['mode'] == 'train':
                trn_list += [line_as_dict]

            # Validation log as list of dictionaries
            if line_as_dict['mode'] == 'val':
                val_list += [line_as_dict]

    # CSV file names
    json_dir = os.path.dirname(argd['json_path'])
    json_name = os.path.splitext(os.path.basename(argd['json_path']))[0]
    trn_csv_fpath = f"{json_dir}/{json_name}_trn.csv"
    val_csv_fpath = f"{json_dir}/{json_name}_val.csv"

    # Write csv files
    trn_df = pd.DataFrame(trn_list)
    val_df = pd.DataFrame(val_list)
    trn_df.to_csv(trn_csv_fpath)
    val_df.to_csv(val_csv_fpath)



# Execution starts here
if __name__ == "__main__":
    main()
