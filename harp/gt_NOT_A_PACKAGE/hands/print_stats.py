import pdb
import pandas as pd
import numpy as np
import sys

if( len(sys.argv) != 2):
    print("USAGE:\n\t python3 comparision.py <video path> <tracking methods> <obj name> <bbox>\n")
    sys.exit(1)

df =  pd.read_csv(sys.argv[1])
sess_row= pd.DataFrame()
grp_row = pd.DataFrame()

for i, row in df.iterrows():
    new_row = row.filename.split("_q2")[0]
    new_row= pd.DataFrame({"filename" : new_row}, index=[0])
    sess_row = sess_row.append(new_row)
for i, row in sess_row.iterrows():
     grp_name = row.filename.split("-")
     grp_name =grp_name[0]+"-"+grp_name[1]+"-"+grp_name[3]
     grp_name_row= pd.DataFrame({"filename" : grp_name}, index=[0])
     grp_row = grp_row.append(grp_name_row)
        #pdb.set_trace()

print("Numer of groups:" ,  len(np.unique(grp_row)))
print("Numer of sessions:" ,  len(np.unique(sess_row)))
print("Number of instances of hand:" , len(df.filename))
print("Numebr of images:",len(np.unique(df.filename)))
