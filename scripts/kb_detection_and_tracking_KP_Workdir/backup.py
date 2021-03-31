import cv2
import sys
import pandas as pd
import pdb
import os
import math

#Parsing methods
if( len(sys.argv) != 6):
    print("USAGE:\n\t python3 comparision.py <video path> <tracking methods> <obj name> <bbox> <detection.csv>\n")
    print("USAGE: \n\t 'BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT'")
    print("OUTPUT:\n\t <video name><methodname><obj name>.csv\n")
    print("NOTE:\n\t Do not use spaces and double underscores in object name\n")
    sys.exit(1)


#Read Detectiopn csv file
det_df = pd.read_csv(sys.argv[5],index_col=False)


#(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')￼
(major_ver, minor_ver) = cv2.__version__.split(".")[:2]



if __name__ == '__main__' :

    # Set up tracker.
    # Instead of MIL, you can also use
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = sys.argv[2]


    if tracker_type == 'BOOSTING':
        tracker = cv2.TrackerBoosting_create()
    if tracker_type == 'MIL':
        tracker = cv2.TrackerMIL_create()
    if tracker_type == 'KCF':
        tracker = cv2.TrackerKCF_create()
    if tracker_type == 'TLD':
        tracker = cv2.TrackerTLD_create()
    if tracker_type == 'MEDIANFLOW':
        tracker = cv2.TrackerMedianFlow_create()
    if tracker_type == 'GOTURN':
        tracker = cv2.TrackerGOTURN_create()
    if tracker_type == 'MOSSE':
        tracker = cv2.TrackerMOSSE_create()
    if tracker_type == "CSRT":
        tracker = cv2.TrackerCSRT_create()

#loop through detection
#sravani

    for index,row in det_df.iterrows():
        bbox = (row['w0'],row['h0'],row['w'],row['h'])
        pdb.set_trace()
        print("sravani")

    # Read video
    video = cv2.VideoCapture(sys.argv[1])

    # Exit if video not opened.
    if not video.isOpened():
        print ("Could not open video")
        sys.exit()

    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print ('Cannot read video file')
        sys.exit()

    # Calculating frames to skip
    fps = round(video.get(cv2.CAP_PROP_FPS))
    #skip_sec = 1/120
    fr_to_sk = fps

    # Define an initial bounding box
    #bbox = sys.argv[4]
    #bbox = tuple(int(x) for x in sys.argv[4].split(","))
    #pdb.set_trace()
    #bbox = (211,267,175,61)

    # Uncomment the line below to select a different bounding box
    bbox = cv2.selectROI(frame, False)

    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)

    bbox_list=[]
    poc=0

    bbox = [bbox[0], bbox[1], bbox[2], bbox[3]]
    bbox = [poc] + bbox
    bbox_list = bbox_list + [bbox]
    poc  = poc + fr_to_sk
    while True:
        # Read a new frame
        video.set(cv2.CAP_PROP_POS_FRAMES,poc)
        ok, frame = video.read()
        if not ok:
            break

        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        ok, bbox = tracker.update(frame)
        pdb.set_trace()
        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

        # Draw bounding box
        if ok:
            # Tracking success
            bbox=list(bbox)
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)

            bbox = [poc] + bbox
            bbox_list = bbox_list + [bbox]



            poc  = poc + fr_to_sk
            video.set(cv2.CAP_PROP_POS_FRAMES,poc)
            fr_suc, fr = video.read()

        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            bbox = list((-1,-1,-1,-1))
            bbox = [poc] + bbox
            bbox_list = bbox_list + [bbox]
            poc  = poc + fr_to_sk
            video.set(cv2.CAP_PROP_POS_FRAMES,poc)
            fr_suc, fr = video.read()

        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);

        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

        # Display result
        cv2.imshow("Tracking", frame)

        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break

# Create a dataframe out of list and save it
bbox_df = pd.DataFrame(bbox_list,
                       columns=['poc','x','y','w','h'])

# Saving ground truth as csv file.
base_name = os.path.basename(sys.argv[1])
vid_name  = os.path.splitext(base_name)[0] + "__" + sys.argv[2] + "__" + sys.argv[3] + ".csv"
print(vid_name)
bbox_df.to_csv(vid_name,index=False)
