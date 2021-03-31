"""
Description
-----------
Creates a csv file with bounding boxes that contain hands.

Example
-------
```
python test_video.py <config file> <ckpt file> <video> <threshold>
```

python test_video.py
/home/sravani/Dropbox/steeparthi/HARP-root/software/sravani-git/HARP/mmdetection/hands/configs/faster-rcnn/two_aug/aolme_hands_faster_rcnn.py
/home/sravani/Softwares/open-mmlab/mmdetection/work_dir/two_aug/epoch_20.pth
/home/sravani/Dropbox/typing-notyping/C1L1P-E/20170302/G-C1L1P-Mar02-E-Irma_q2_03-08_30fps.mp4
0.5 /mnt/threetb/mmdetection/out_videos/
"""
import argparse
from mmdet.apis import init_detector, inference_detector, show_result_pyplot
import pdb
import mmcv
import cv2
import numpy as np
import pandas as pd

def _arguments():
    """Parses input arguments."""

    # Initialize arguments instance
    args_inst = argparse.ArgumentParser(
        description=("""Script description goes here"""))

    # Adding arguments
    args_inst.add_argument("config_file",
        type=str,
        help=("<The same configuration file which is used for training>"))

    args_inst.add_argument("ckpt_file",
        type=str,
        help=("trained checkpoint file"))

    args_inst.add_argument("video",
        type=str,
        help=("<Video path>"))

    args_inst.add_argument("th",
        type=str,
        help=("<Threshold for the model>"))

    args_inst.add_argument("out_pth",
        type=str,
        help=("<output path to save video and csv files>"))
    args = args_inst.parse_args()

    # Crate a dictionary having arguments and their values
    args_dict = {'config_file': args.config_file , 'ckpt_file':args.ckpt_file,
                'video':args.video, 'th':args.th, 'out_pth':args.out_pth}

    # Return arguments as dictionary
    return args_dict


def main():
    """Main function."""
    argd = _arguments()
    print(argd)
    config_file = argd['config_file']
    checkpoint_file = argd['ckpt_file']
    video = argd['video']
    th = argd['th']
    th = float(th)
    out_pth = argd['out_pth']
    skp_frms = 30

    device = 'cuda:0'

    # init a detector
    model = init_detector(config_file, checkpoint_file, device=device)


    # test a video and show the results
    cap = cv2.VideoCapture(video)
    font = cv2.FONT_HERSHEY_SIMPLEX
    poc = 0
    vname = video.split("/")[-1].split(".")[0]
    #out = cv2.VideoWriter(out_pth + vname + "_det_per_sec.mp4",cv2.VideoWriter_fourcc('M','J','P','G'), 30, (858,480))
    detrows = []

    ret,frame = cap.read()
    while(cap.isOpened()):
        if np.sum(frame) !=None :
            result = inference_detector(model, frame)

            l =  len(result[0])
            for i in range(0,l):
                bbox = result[0][i]
                xmin = bbox[0]
                ymin = bbox[1]
                xmax = bbox[2]
                ymax = bbox[3]
                score =bbox[4]

                if score > th:
                    #cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (0,255,0), 2)
                    score  = np.round(score,2)
                    #cv2.putText(frame,'hand|'+ str(score),(xmin,ymin), font,0.6 , (0, 255, 0), 2, cv2.LINE_AA)
                    detrows    = detrows + [[poc,858,480,30, int(xmin), int(ymin), int(xmax-xmin), int(ymax-ymin)]]
            #out.write(frame)
            #cv2.imshow("image", frame)
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break
            poc += skp_frms

            cap.set(cv2.CAP_PROP_POS_FRAMES, poc)
            ret, frame     = cap.read()
        else:
            break
    cap.release()
    #out.release()
    cv2.destroyAllWindows()

    print("Done writing")
    detdf = pd.DataFrame(detrows, columns=["poc","W","H","FPS","w0","h0","w","h"])
    detdf.to_csv(out_pth + vname + "_one_det_per_sec.csv", index=False)

# Execution starts here
if __name__ == "__main__":
    main()
