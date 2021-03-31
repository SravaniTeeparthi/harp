# MMDETECTION
## Installation
Please refer to Dockerhub page for further information.
+ Date: Mar 01, 2021
+ Official link: [Github repo](https://github.com/open-mmlab/mmdetection/blob/master/docs/get_started.md).
+ Prerequisites: `docker` and `nvidia-docker`
+ Dockerhub: [Docker hub](https://hub.docker.com/repository/docker/venkatesh369/mmdetection)

## Usage
Starting docker container
```bash
sudo docker run --name mmdet --gpus 1 --shm-size 24G -it -v /home/vj/DockerHome/mmdetection:/home venkatesh369/mmdetection:working
```
### Training
Learning rate needs to be decreased to accomidate for 1 GPU. They
```bash
# From mmdetection directory (worked on rtx3 system)
python tools/train.py /home/sravani/Dropbox/steeparthi/HARP-root/software/vj-HARP/mmdetection-configs/hands/faster-rcnn/aolme_hands_faster_rcnn.py --work-dir /home/sravani/Softwares/open-mmlab/mmdetection/work_dirs/temp
```
### Testing
The following script tests images with bounding boxes defined in json format.
```bash
# From mmdetection directory (worked on rtx3 system)
python tools/test.py /home/sravani/Dropbox/steeparthi/HARP-root/software/vj-HARP/mmdetection-configs/hands/faster-rcnn/aolme_hands_faster_rcnn.py /home/sravani/Softwares/open-mmlab/mmdetection/work_dirs/temp/latest.pth --eval bbox
```
### Visualization
1. Visualize bounding boxes on images
To visualize bounding boxes on a test image use the script provided at `mmdetection/test_scripts/test_image.py`
```bash
# Argumetns
python test_image.py <config file> <ckpt file> <image> <threshold>

# Example: Plotting hand bounding boxes (worked on rtx3 system)
CUDA_VISIBLE_DEVICES=0 python test_image.py /home/sravani/Dropbox/steeparthi/HARP-root/software/vj-HARP/mmdetection/hands/configs/faster-rcnn/no_aug/aolme_hands_faster_rcnn.py /home/sravani/Softwares/open-mmlab/mmdetection/work_dir/no_aug/latest.pth /home/sravani/Dropbox/steeparthi/HARP-root/data/hand_detection/images/G-C1L1P-Mar30-C-Kelly_q2_06-06_30fps_poc_12966.png 0.3
```
2. Visualize bounding boxes on video
