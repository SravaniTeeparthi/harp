"""
Description
-----------
Draws hand bounding boxes on an image. It also prints confidence
score on top of the box.

Example
-------
```
python test_image.py <config file> <ckpt file> <image> <threshold>
```
"""
import argparse
from mmdet.apis import init_detector, inference_detector, show_result_pyplot
import pdb

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

    args_inst.add_argument("img_pth",
        type=str,
        help=("<Test Image>"))

    args_inst.add_argument("th",
        type=str,
        help=("<Threshold for the model>"))
    args = args_inst.parse_args()

    # Crate a dictionary having arguments and their values
    args_dict = {'config_file': args.config_file , 'ckpt_file':args.ckpt_file,
                'img_pth':args.img_pth, 'th':args.th}

    # Return arguments as dictionary
    return args_dict


def main():
    """Main function."""
    argd = _arguments()
    print(argd)
    config_file = argd['config_file']
    checkpoint_file = argd['ckpt_file']
    img = argd['img_pth']
    th = argd['th']
    th = float(th)

    device = 'cuda:0'

    # init a detector
    model = init_detector(config_file, checkpoint_file, device=device)

    # inference the demo image
    result = inference_detector(model, img)
    show_result_pyplot(model, img, result, score_thr=th)

# Execution starts here
if __name__ == "__main__":
    main()
