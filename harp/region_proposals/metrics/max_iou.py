"""
Calcualtes performance of region proposals. Please refer `Max IoU` section
in the README for more details.
"""

import pandas as pd
import harp.fdops as fdops


class MaxIoU:
    """
    Calculates region propsal performance. This assumes that the proposals
    are bounding boxes. Please refer `Max IoU` section in the README for details.
    """

    _gt_df = pd.DataFrame()
    _prop_df = pd.DataFrame()

    def __init__(self, gt_csv, proposals_dir):
        """
        Creates an instance of MaxIoU.

        Parameters
        ----------
        gt_csv : str
            Ground truth csv file
        proposals_dir : str
            Directory having region proposals(one csv file for a video)
        """

        # Checking for existance
        fdops.check_if_file_exists(gt_csv)
        fdops.check_if_dir_exists(proposals_dir)

        # Loading ground truth csv file
        self._gt_df = pd.read_csv(gt_csv)

        # Loading proposals dataframe
        prop_csvs = fdops.get_file_list(proposals_dir, "csv")
        for idx, prop_csv in enumerate(prop_csvs):

            # Get current video name
            vid_name = self._get_vid_name(prop_csv)

            temp_df = pd.read_csv(prop_csv)
            if idx == 0:
                self._prop_df = temp_df
            else:
                self._prop_df = pd.concat([self._prop_df, temp_df])

    def _get_vid_name(self, prop_csv_pth):
        """ Returns video name by parsing csv file.

        Parameters
        ----------
        prop_csv_pth : str
            Proposal csv file path
        """


if __name__ == "__main__":
    gt_csv = ("/home/vj/data/Dropbox/writing-nowriting-GT/C1L1P-C/20170330/"
              "gTruth-wnw_30fps.csv")
    proposals_dir = ("/home/vj/data/Dropbox/objectdetection-aolme/"
                     "hand-mmaction2/faster-rcnn/C1L1P-C/20170330")
    perf_max_iou = MaxIoU(gt_csv, proposals_dir)
