# Faster RCNN configurations
The following directory contains configurations used to run data augmentation at
different levels.
1. **no_aug**:
   No augmentation
2. **one_aug**:
   1. Horizontal flip with probability of 0.5
3. **two_aug**:
   1. Horizontal flip with probability of 0.5
   2. Scaling with sacale factior [0.8, 1.2]
4. **three_aug**:
   a. With shear
	   1. Horizontal flip with probability of 0.5
	   2. Scaling with sacale factior [0.8, 1.2]
	   3. Shear between [-45, 45] with 0.5 probability for negative.
   b. Without Shear
       1. Horizontal flip with probability of 0.5
	   2. Scaling with sacale factior [0.8, 1.2]
	   3. Rotate between [-45, 45] with 0.5 probability.
5. **four_aug**:
   1. Horizontal flip with probability of 0.5
   2. Scaling with sacale factior [0.8, 1.2]
   3. Shear between [-45, 45] with 0.5 probability for negative.
   4. Rotate between [-45, 45] with 0.5 probability.
6. **five_aug**:
   1. Horizontal flip with probability of 0.5
   2. Scaling with sacale factior [0.8, 1.2]
   3. Shear between [-0.3, 0.3] with 0.5 probability for negative.
   4. Rotate between [-10, 10] with 0.5 probability.
   5. Translate horizontally between [-10,10] pixels.
