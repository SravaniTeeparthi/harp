# Object detection projections
## Files
1. `projections.py` <-- Module
   The following module contians a class with methods that creates
   and visualizes bounding box projections.
2. `create_projection_masks.py` <-- Script
   The following script uses `projections.py` to write projects as png
   images for every 12 seconds.
3. `write_projections_on_video.py` <-- Script
   This script creates a video with projection mask overlayed on frames.
   The overlay happens every second.
