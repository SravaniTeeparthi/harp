# The new config inherits a base config to highlight the necessary modification
_base_ = './faster_rcnn_r101_fpn_1x_coco.py'



# We also need to change the num_classes in head to match the dataset's annotation
model = dict(
    roi_head=dict(
        bbox_head=dict(num_classes=1)))

# Modify dataset related settings
dataset_type = 'COCODataset'
classes = ('hand',)
data = dict(
    samples_per_gpu=2, # mini batch size
    workers_per_gpu=2,
    train=dict(
        img_prefix='/home/sravani/Dropbox/steeparthi/HARP-root/data/hand_detection/images/',
        classes=classes,
        ann_file='/home/sravani/Dropbox/steeparthi/HARP-root/data/hand_detection/coco-format/all/trn.json'),
    val=dict(
        img_prefix='/home/sravani/Dropbox/steeparthi/HARP-root/data/hand_detection/images/',
        classes=classes,
        ann_file='/home/sravani/Dropbox/steeparthi/HARP-root/data/hand_detection/coco-format/all/val.json'),
    test=dict(
        img_prefix='/home/sravani/Dropbox/steeparthi/HARP-root/data/hand_detection/images/',
        classes=classes,
        ann_file='/home/sravani/Dropbox/steeparthi/HARP-root/data/hand_detection/coco-format/all/tst.json'))

# We can use the pre-trained Mask RCNN model to obtain higher performance
load_from = '/home/sravani/Softwares/open-mmlab/mmdetection/checkpoints/faster_rcnn_r101_fpn_1x_coco_20200130-f513f705.pth'
