# Region proposal metrics
## Max IoU
* IoU ratio is calculated for each  detection and ground truth activity.
* The detection which gives max detection is considered.
* Suppose there are 5 detections (d1, d2, d3, d4, d5) and Ground truth (g)
* Max (IoU(d1,g), IoU(d2,g), IoU(d3,g), IoU(d4,g), IoU(d5,g) )

![](iou_calculation.PNG)
