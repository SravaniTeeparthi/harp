_base_ = [
    './faster_rcnn_r50_fpn.py', # Model
    './coco_detection.py', # Dataset
    './schedule_1x.py', # Schedule
    './default_runtime.py' # runtime
]
