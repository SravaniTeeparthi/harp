from projections import BBoxProjections

# directories for which we need projections
indirs = [
    ("/home/vj/Dropbox/objectdetection-aolme/hand-mmaction2/"
     "faster-rcnn/C1L1P-C/20170330/")
    ]

# Loop over each directory and get csv files

# Linux
csv_loc = ("/home/vj/Dropbox/objectdetection-aolme/hand-mmaction2/"
           "faster-rcnn/C1L1P-C/20170330/"
           "G-C1L1P-Mar30-C-Kelly_q2_01-06_30fps_det_per_sec.csv")

# Initialize projection instance
proj = BBoxProjections(csv_loc, proj_interval=12, det_interval=1)

# Creating projection png images
proj.create_images()
