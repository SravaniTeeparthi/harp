"""
Description
-----------
The will parse the json file produced during training and prints best epoch.
We consider best epoch to have highest validation accuracy.

Example
-------
```
python get_best_epoch.py <path to json file>
```
"""
import pdb
import argparse
import json


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

    """ Load json file to a list. Each element is a line """
    with open(argd['json_path']) as f:
        content = f.readlines()
        content = [x.strip() for x in content]

    """ Loop through each line and create validation array """
    best_val_map_50 = 0
    val_map_50_lst = []
    for lidx, line in enumerate(content):
        line_as_dict = json.loads(line)

        if 'mode' in line_as_dict.keys():

            if line_as_dict['mode'] == 'val':
                val_map_50 = line_as_dict['bbox_mAP_50']
                val_map_50_lst += [val_map_50]

                if val_map_50 >= best_val_map_50:
                    best_epoch_dict = line_as_dict
                    best_val_map_50 = val_map_50

    print(best_epoch_dict)
    print(max(val_map_50_lst))


# Execution starts here
if __name__ == "__main__":
    main()
