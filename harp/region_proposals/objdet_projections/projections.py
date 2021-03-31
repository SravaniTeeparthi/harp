"""
The following module contians a class with methods that creates, saves
and visualizes bounding box projections.
"""


import os
import sys
import pdb
import cv2
import glob
import math
import shutil
import skvideo.io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from progressbar import ProgressBar
from os.path import splitext as splitext
from os.path import basename as basename




class BBoxProjections:
    """
    Methods to create bounding box projections. The input is a csv
    file having bounding boxes. It has following columns
    `f0, W, H, FPS, w0, h0, w, h`,
    + f0      = POC of video frame
    + W       = Width of video frame
    + H       = Height of video frame.
    + FPS     = Frame rate
    + (w0,h0) = top left corner, (width, height) direction.
    + (w,h)   = Bounding box wiht and height
    """

    def __init__(self, csv_loc, proj_interval=12, det_interval=1):
        """ Initializes boundin box projections instance.

        Parameters
        ----------
        csv_loc : str
            Location of CSV file havin bounding boxes
        proj_interval : int, default 12
            Projections are calculated for every `proj_interval`
            seconds.
        det_interval  : int, default 1
            Detection interval to consider in calculating projections.
            For example if this value is 1 then we consider 1
            detection per second to calculate projections.
        """
        # CSV exists?
        if not os.path.isfile(csv_loc):
            raise Exception(
                f"USER_EXCEPTION: File does not exist \n\t{csv_loc}"
            )

        # CSV file info
        csv_name = os.path.splitext(os.path.basename(csv_loc))[0]
        csv_dir  = os.path.dirname(csv_loc)
        self._csv_props = {
            'name': csv_name,
            'dir': csv_dir
        }

        # Load csv as data frame
        self._df = pd.read_csv(csv_loc)

        # Other importatnt parameters
        self._proj_interval = proj_interval
        self._det_interval = det_interval


    def create_images(self):
        """
        Writes projections to png images. All images are placed under
        a directory having same name as csv file. The directory is
        located in the same directory as csv file.
        """
        # Deleting old dir and creating a new one
        masks_dir = (
            f"{self._csv_props['dir']}/{self._csv_props['name']}"
        )
        if os.path.isdir(masks_dir):
            shutil.rmtree(masks_dir)
        os.mkdir(masks_dir)

        # Setting up loop parameters
        FPS = self._df['FPS'].unique().item()
        W = self._df['W'].unique().item()
        H = self._df['H'].unique().item()

        f0min = self._df['f0'].min()
        f0max = self._df['f0'].max()

        fp_step = FPS*self._proj_interval
        f0s_p = [*range(f0min, f0max, fp_step)] # f0 for projection

        # Projection loop
        for i in range(len(f0s_p)-1):

            # Creating an empty image
            img = np.zeros((H,W))

            # Starting and ending frame numbers of projection
            f0_p_start = f0s_p[i]
            f0_p_end = f0s_p[i+1] - 1


            # Data frame with only current projection frame data
            dfp = self._df[self._df['f0'] >= f0_p_start].copy()
            dfp = dfp[dfp['f0'] < f0_p_end].copy()

            fd_step = FPS*self._det_interval
            f0s_d = [*range(f0_p_start,f0_p_end,fd_step)]

            # Detection loop
            for j in range(len(f0s_d)-1):
                df0 = dfp[dfp['f0'] == f0s_d[j]].copy()

                # BBox loop per frame
                for ridx, row in df0.iterrows():

                    w0, h0 = row['w0'], row['h0']
                    w, h = row['w'], row['h']

                    temp_img = np.zeros((H,W))
                    temp_img[h0:h0+h, w0:w0+w] = 1

                    img += temp_img

            # Saving image in directory
            img_postfix = f"_{f0_p_start}_{f0_p_end}.png"
            img_name = (
                f"{self._csv_props['name']}{img_postfix}"
            )
            img_fpath = f"{masks_dir}/{img_name}"

            # Normalizing image
            img = 255*(img/img.max())

            # Write image
            print(f"USER_INFO: Saving {img_fpath}")
            cv2.imwrite(img_fpath, img)


    def mask_video_with_projections(self, vid_file, frms_per_sec=1):
        """
        Masks video with projections(png images). Images are gray
        scales with intensity representing probability of finding
        an object(hand or keyboard in our case).

        This method also assumes that the image file name has
        POC(f0) information. For example:
        `G-C1L1P-Mar30-C-Kelly_q2_01-06_30fps_det_per_sec_0_359.png`
        means that this projection mask is applied from POC 0 to
        359.

        Parameters
        ----------
        vid_file : str
            Video for which we are creating the mask
        frms_per_sec : int, default 1
            Number of frames to project per second

        """
        # Opencv blending parameters
        alpha = 0.3
        beta = 1-alpha

        # Directories and files we are going to process
        csv_name = self._csv_props['name']
        csv_dir = self._csv_props['dir']
        masks_dir = f"{csv_dir}/{csv_name}"
        if not os.path.isdir(masks_dir):
            raise Exception (
                "USER_EXEPTION: Directory doesn't exist\n\t"
                f"{masks_dir}")

        # Creating an array having all the mask_files
        mask_files = glob.glob(f"{masks_dir}/*.png")

        # Loading video and its properties
        vr = cv2.VideoCapture(vid_file)
        nfrms = int(vr.get(cv2.CAP_PROP_FRAME_COUNT))

        # POC number of frames under consideration
        fps = 30
        f0s = list(range(0,nfrms,frms_per_sec*fps))

        # Creating scikit video writer
        vw_file = f"{masks_dir}/{csv_name}_masked.mp4"
        vw = skvideo.io.FFmpegWriter(vw_file, outputdict={
            '-vcodec': 'libx264',
            '-r':'30'})

        # Loop over each frame
        pbar = ProgressBar()
        for f0 in pbar(f0s):

            # Loading approprite mask
            mask_img = self._load_current_mask_image(f0, mask_files)

            vr.set(cv2.CAP_PROP_POS_FRAMES, f0)
            ret, fr = vr.read()

            # Combine mask and image
            masked_frm = cv2.addWeighted(fr, alpha, mask_img, beta, 0.0)
            masked_frm = cv2.cvtColor(masked_frm, cv2.COLOR_BGR2RGB)

            # writing frame
            vw.writeFrame(masked_frm)

        # Closing vr and vw
        vr.release()
        vw.close()

    def _load_current_mask_image(self, poc, mask_files):
        """ Returns approprite mask for poc under consideration

        Parameters
        ----------
        poc : int
            POC of frame we need mask for
        mask_files : list of str
            List of paths having mask file names
        """
        for cmask_path in mask_files:
            mask_name = splitext(basename(cmask_path))[0]
            fs = int(mask_name.split("_")[-2])
            fe = int(mask_name.split("_")[-1])
            if fs <= poc and poc <= fe:
                mask_img = cv2.imread(cmask_path).astype('uint8')
                return mask_img


        # If there is no mask 0 mask
        print(f"There is no mask for {poc}, writing zero mask.")
        first_mask = cv2.imread(mask_files[0])
        zero_mask = np.zeros(first_mask.shape).astype('uint8')
        return zero_mask


if __name__ == "__main__":
    # Linux
    csv_loc = ("/home/vj/Dropbox/objectdetection-aolme/hand-mmaction2/"
               "faster-rcnn/C1L1P-C/20170330/"
               "G-C1L1P-Mar30-C-Kelly_q2_01-06_30fps_det_per_sec.csv")

    # Initialize projection instance
    proj = BBoxProjections(csv_loc, proj_interval=12, det_interval=1)

    # Creating projection png images
    # proj.create_images()

    # Blending projection images with
    proj.mask_video_with_projections(
        "/home/vj/Dropbox/writing-nowriting-GT/C1L1P-C/20170330/"
        "G-C1L1P-Mar30-C-Kelly_q2_01-06_30fps.mp4"
    )
