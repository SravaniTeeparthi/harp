"""
Description
-----------
For every second of video, check if there are any writing instances.
If atleast 50% of the frames have writing then save the instance to csv file.

for all the writing Instances, get hands from the frames and calculate
IoU ratios of each detection with wriitng ground truth. Take the max IoU
ratio and save the csv file.
Classify as succes or failure
Example
-------
```
```
"""
import os
import pandas as pd
import pdb



class Performance:
    # Class variables
    _gt_csv = None
    _properties_csv = None
    _m_csv = None

    def __init__(self, gt_csv, properties_csv, m_csv, out_pth):
        """
        Initializes Perforamnce instance.

        Parameters
        ----------

        gt_csv = ground truth csv file
        properties_csv  = csv file containing properties of session
        m_csv = csv file of method to which perforamnce needs to be calculated
        output_csv = folder to save csv files
        """
        # Updating class variables
        self._gt_csv = gt_csv
        self._properties_csv = properties_csv
        self._m_csv = m_csv
        self._out_pth = out_pth

    def get_video_properties(self):

        self.v_name        = os.path.splitext(self._m_csv.split("/")[-1])[0]
        prop_df       = pd.read_csv(self._properties_csv)
        video_prop    = prop_df.loc[prop_df['name'] == self.v_name]
        self.W             = int(video_prop.width)
        self.H             = int(video_prop.height)
        self.dur           = int(video_prop.dur)
        self.FPS           = int(video_prop.FPS)



    def bb_intersection_over_union(self,boxA, boxB):
    	# determine the (x, y)-coordinates of the intersection rectangle
    	xA = max(boxA[0], boxB[0])
    	yA = max(boxA[1], boxB[1])
    	xB = min(boxA[2], boxB[2])
    	yB = min(boxA[3], boxB[3])

    	# compute the area of intersection rectangle
    	interArea = max(0,xB - xA+1) * max(0,yB - yA+1)

    	# compute the area of both the prediction and ground-truth rectangles
    	boxAArea = (boxA[2] - boxA[0]+1) * (boxA[3] - boxA[1]+1)
    	boxBArea = (boxB[2] - boxB[0]+1) * (boxB[3] - boxB[1]+1)

    	# compute the intersection over union by taking the intersection
    	# area and dividing it by the sum of prediction + ground-truth
    	# areas - the interesection area
    	iou = interArea / float(boxAArea + boxBArea - interArea)

    	return iou

    def to_csv(self, c_rows):
        f_df = pd.DataFrame(c_rows,columns=["vid_name","f0","f1","kid","w0","h0","w","h","iou","success"])
        f_df.to_csv(self._out_pth+"performance_" +self.v_name+".csv",index=False)


    def get_video_df_from_gt(self):
        p_gtrows = []
        gt_df =  pd.read_csv(self._gt_csv)
        self.get_video_properties()
        vid_df  =gt_df.loc[(gt_df['name'] == self.v_name+".mp4") & (gt_df['activity']=="writing")]

        vid_df['f1'] = vid_df['f0'] + vid_df['f']
        total_frames = int(self.dur * self.FPS)
        fiftyPercFrames = self.FPS / 2
        # Checking evry 30 frames
        for i in range(0,total_frames,30):
            frames = [i,i+30]
            writingInstances = vid_df.loc[ ((vid_df['f0'] <= frames[0])  & (vid_df['f1'] >= frames[1])) |
                ((vid_df['f0'] <= frames[0]) & (vid_df['f1'] <= frames[1])) ]

            if len(writingInstances):
                for i,row in writingInstances.iterrows():
                    frame_num = frames[0]+ fiftyPercFrames
                    # more than 15 frames are writing
                    if (frame_num > row['f0']) & (frame_num < row['f1']):
                        p_gtrows = p_gtrows + [[row['name'],frames[0],frames[1],row['person'],row['w0'],row['h0'],row['w'],row['h']]]

        return p_gtrows



    def cal_iou(self, p_gt_df):
        m_df = pd.read_csv(self._m_csv)
        pf_final_rows = []

        for i,row in p_gt_df.iterrows():
            iou_df = m_df.loc[m_df['f0'] == row['f0']] .append(m_df.loc[m_df['f0'] == row['f1']])
            iou_row = []
            for i, cal in iou_df.iterrows():
                bbox_A=(row['w0'],row['h0'],row['w0']+row['w'],row['h0']+row['h'])
                bbox_B = (cal['w0'],cal['h0'],cal['w0']+cal['w'],cal['h0']+cal['h'])
                iou = self.bb_intersection_over_union(bbox_A,bbox_B)
                iou_row = iou_row + [iou]

            if max(iou_row) > 0.3:
                success = 1
            else :
                success = 0
            pf_final_rows = pf_final_rows + [[row['vid_name'],row['f0'],row['f1'],row["kid"],row['w0'],row['h0'],row['w'],row['h'],max(iou_row),success]]
        return pf_final_rows
