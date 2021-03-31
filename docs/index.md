# Experiments - Hand Detection
## Exp-1

  |   |Number of groups|Number of Sessions| Number of Images | Number of instances of hand | 
  | ----------- | ----------- | --------- | ----------|--------------|
  | train      | 9 | 33 | 305       | 1803   |
  | val        | 4 | 4 | 100       | 714    |
  | test       | 6 | 7 |    313       |   2031    |
  
  
 Method Used: FasterRCNN 
 
  |        |      |
  | ----- | ----------|
  | Time Taken to train | 17min |
  | Number of Epochs |   12   |
  | Number of iterations/Epoch |   153   |
  | Trianing Accuracy |  93.99 |
  |Vlaidation bbox_mAP_50 | 0.793  |
  |Testing bbox_mAP_50 | 0.684  |
  
 Method Used: Yolov3
 
  |  |      |
  | ----- | ----------|
  | Sysytem Used |      |
  | Time Taken to train |1 hr55m  |
   | Number of Epochs |   273   |
  | Number of iterations/Epoch |   39   |
  |Validation bbox_mAP_50 |0.732  |
  |Testing bbox_mAP_50 | 0.663  |
