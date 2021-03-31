"""
Description
-----------
The following script documents hand ground truth properties into a text file with same name
and location as csv file.

Example
-------
```
python save_stats.py \
    ~/Dropbox/steeparthi/HARP-root/data/hand_detection/csv/all/trn.csv
```
"""
import os
import pdb
import argparse
import pandas as pd

def _arguments():
    """Parses input arguments."""

    # Initialize arguments instance
    args_inst = argparse.ArgumentParser(
        description=("""
            The following script documents hand ground truth properties
            into a text file.
            """))

    # Adding arguments
    args_inst.add_argument("gt_csv",
        type=str,
        help=("CSV file having image names and bounding boxes."))
    args = args_inst.parse_args()

    # Crate a dictionary having arguments and their values
    args_dict = {'gt_csv': args.gt_csv}

    # Return arguments as dictionary
    # Hello world how are you doing
    return args_dict


def main():
    """Main function."""
    argd = _arguments()

    if not(os.path.isfile(argd['gt_csv'])):
        raise Exception(f"ERROR: File not fund {argd['gt_csv']}")

    # Open text file for writing
    opth = os.path.dirname(argd['gt_csv'])
    oname = os.path.splitext(os.path.basename(argd['gt_csv']))[0]+".txt"
    otxt = f"{opth}/{oname}"
    f = open(otxt,"w")

    gtdf = pd.read_csv(argd['gt_csv'])
    fnames = gtdf['filename'].tolist()



    # Loop over each image
    glist = []
    slist = []
    for fname in fnames:
        glist += [f"{fname.split('-')[1]}-{fname.split('-')[3]}"]
        slist += [f"{fname.split('-')[1]}-{fname.split('-')[2]}-{fname.split('-')[3]}"]

    # Add the two columns to the data frame
    gtdf['group'] = glist
    gtdf['session'] = slist


    # Writing totals
    print("Total", file=f)
    print(f"    Unique instances: {len(gtdf)}", file=f)
    print(f"    Unique images:    {len(gtdf['filename'].unique())}", file=f)
    print(f"    Unique groups:    {len(gtdf['group'].unique())}", file=f)
    print(f"    Unique sessions:  {len(gtdf['session'].unique())}", file=f)
    print(f"---      MORE DETAILS BELOW      ---\n", file=f)

    # Group loop
    uniq_groups = gtdf['group'].unique()
    for g in uniq_groups:
        cg_df = gtdf[gtdf['group'] == g]
        cg_uniq_sess = cg_df['session'].unique()
        cg_uniq_images = cg_df['filename'].unique()

        # Printing group info to text file
        print(f"Group: {g}", file=f)
        print(f"    Hand instances:       {len(cg_df)}", file=f)
        print(f"    Unique images:        {len(cg_uniq_images)}", file=f)
        print(f"    Sessions:             {len(cg_uniq_sess)}", file=f)
        print(f"Group: {g}")
        print(f"    Hand instances:       {len(cg_df)}")
        print(f"    Unique images:        {len(cg_uniq_images)}")
        print(f"    Sessions:             {len(cg_uniq_sess)}")


        # Session loop
        for s in cg_uniq_sess:
            cs_df =cg_df[cg_df['session'] == s]
            cs_uniq_images = cs_df['filename'].unique()

            # Printing session info to text file
            print(f"        Session: {s}", file=f)
            print(f"            Hand instances:       {len(cs_df)}", file=f)
            print(f"            Unique images:        {len(cs_uniq_images)}", file=f)
            print(f"        Session: {s}")
            print(f"            Hand instances:       {len(cs_df)}")
            print(f"            Unique images:        {len(cs_uniq_images)}")

    f.close()




# Execution starts here
if __name__ == "__main__":
    main()
