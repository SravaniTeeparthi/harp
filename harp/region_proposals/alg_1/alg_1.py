import cv2
import pdb
import numpy as np
import os
import pandas as pd
from harp import fdops
from natsort import os_sorted


class Alg1:

    # Class variables
    _img_pth = None
    _properties_csv = None

    def __init__(self, img_pth, properties_csv, out_pth):
        """
        Initializes alg_1 region proposal  instance.

        Parameters
        ----------

        proj_path = folder conmtaining projected image_conversions
        properties_csv  = csv file containing properties of session
        output_csv = folder to save csv files
        """
        # Updating class variables
        self._img_pth = img_pth
        self._properties_csv = properties_csv
        self._out_pth = out_pth

    def get_video_properties(self):
        self.v_name        = self._img_pth.split("/")[-2].split("_30fps")[0] + "_30fps"
        prop_df       = pd.read_csv(self._properties_csv)
        video_prop    = prop_df.loc[prop_df['name'] == self.v_name]
        W             = int(video_prop.width)
        H             = int(video_prop.height)
        dur           = int(video_prop.dur)
        FPS           = int(video_prop.FPS)
        return W,H,dur,FPS

    def bbox(self, x,y):
        w = 122
        h = 79
        xmin,ymin = (x - (w * 0.5), y - (h * 0.5))
        xmax, ymax = (x + (w * 0.5), y + (h * 0.5))
        return int(xmin),int(ymin),int(xmax),int(ymax)

    def proposals_to_csv(self, c_rows):
        f_df = pd.DataFrame(c_rows,columns=["W","H","fps","dur","f0","f1","nprops","props"])
        f_df.to_csv(self._out_pth+ self.v_name+".csv",index=False)

    def proj_to_proposal(self):
        f1 = int(os.path.splitext(self._img_pth)[0].split("_")[-1])
        f0 = int(os.path.splitext(self._img_pth)[0].split("_")[-2])
        f_row  = []
        img = cv2.imread(self._img_pth,0)
        img_binary = cv2.threshold(img, 25, 255, cv2.THRESH_BINARY)[1]
        erosion = cv2.erode(img_binary,cv2.getStructuringElement(cv2.MORPH_RECT,(7,7)),iterations = 3)

        ## Uncomment to view labelled image
        # num_labels, labels = cv2.connectedComponents(erosion)
        # # Map component labels to hue val, 0-179 is the hue range in OpenCV
        # label_hue = np.uint8(179*labels/np.max(labels))
        # blank_ch = 255*np.ones_like(label_hue)
        # labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
        # # Converting cvt to BGR
        # labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
        # # set bg label to black
        # labeled_img[label_hue==0] = 0

        # apply connected component analysis to the thresholded image
        output = cv2.connectedComponentsWithStats(erosion, 8 , cv2.CV_32S)
        (numLabels, labels, stats, centroids) = output
        row = ""
        for i in range(0,len(centroids)):
            x,y = centroids[i][0],centroids[i][1]
            xmin,ymin,xmax,ymax =self.bbox(x,y)
            row += str(xmin)+"-"+str(ymin)+"-"+str(122)+"-"+str(79)+":"
            ## Uncomment to view labelled image
            #labeled_img = cv2.rectangle(labeled_img, (xmin,ymin), (xmax,ymax), (0, 255, 0), 2)

        W,H, dur,FPS = self.get_video_properties()
        f_row = f_row + [W,H,FPS,dur,f0,f1,len(centroids),row]
        return f_row
