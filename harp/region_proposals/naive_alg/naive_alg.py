import pdb
import pandas as pd
from harp import fdops
from harp.data_processors.detection_data_processor import DetectionData


class NaiveAlg:
    """
    A naive way to propose regions for acitvity classification
    (writing, typing) using object detection results.

    Please refer the README for more information on the algorithm.
    """

    # Class variables
    _dd = None
    _naive_interval = None

    def __init__(self, csv_path, naive_interval=3):
        """
        Initializes naive region proposal algorithm instance.

        Parameters
        ----------
        csv_path : str
            Path to csv file containing detection information
        naive_interval : int, defaults 3
            Time in seconds considered when producing naive
            proposals.
        """
        # Create DetectionData instance
        self._dd = DetectionData(csv_path)

        # Updating class variables
        self._naive_interval = naive_interval

    def to_csv(self, out_dir):
        """
        Writes a csv file with naive proposals. The csv file has
        following columns,
        ```
        W        : Video width
        H        : Video height
        FPS      : Frames per second
        dur      : Duration of current video
        f0       : Starting frame
        f        : Number of frames in proposal interval
        nprops   : Number of proposals
        props    : Proposal boxes, "w0-h0-w-h:w0-h0-w-h:..."
        ```

        Parameters
        ----------
        out_dir : str
            Output directory
        """

        # Checking if the base output directory exists
        fdops.check_if_dir_exists(out_dir)

        # Creating output directory

        # Creating list of f0 and f
        f0_list, f = self._get_list_of_f0s()

        # Loop through each proposal interval
        proposals = []
        pdb.set_trace()
        for i, f0 in enumerate(f0_list):
            crow = [
                self._dd.props['W'], self._dd.props['H'],
                self._dd.props['FPS'], self._dd.props['dur']
            ]

            # Make output directory
            crow += [f0, f]

            # Get proposal bounding boxes string and number of bounding boxes
            crow += self._get_proposal_boxes(f0, f)

            proposals += [crow]

        # Create data frame
        csv_columns = ["W", "H", "FPS", "dur", "f0", "f", "nprops", "props"]
        df = pd.DataFrame(proposals, columns=csv_columns)

        # Create output directory if id does not exist
        out_dir = f"{out_dir}/{self._dd.props['dets_per_sec']}_det_per_sec"
        fdops.recursive_mkdir(out_dir)

        # Save the dataframe as csv file
        out_csv_name = (f"{self._dd.props['vname']}_{self._naive_interval}sec_"
                        "interal.csv")
        out_csv_fpth = f"{out_dir}/{out_csv_name}"
        df.to_csv(out_csv_fpth)

    def _get_list_of_f0s(self):
        """
        Returns a list of f0s(starting frame poc) for which we will be computing
        proposals, and number of frames in each proposal interval.

        """
        f0start = 0
        f0end = self._dd.props['f0_last']
        FPS = self._dd.props['FPS']
        frms_in_prop_int = FPS*self._naive_interval
        f0s = list(range(f0start, f0end, frms_in_prop_int))
        return f0s, frms_in_prop_int

    def _get_proposal_boxes(self, f0, f):
        """ Creates a string that contains all the bounding boxes proposals between
        frames f0 and f.

        Parameters
        ----------
        f0 : int
        POC of first frame for current proposal instance
        f : int
        Number of frames we are considering in current proposal instance
        """

        # Crete a data frame with bounding boxes inside frame interval
        det_df = self._dd._df.copy()
        temp_cdf = det_df[det_df['f0'] >= f0].copy()
        cdf = temp_cdf[temp_cdf['f0'] < (f0+f)].copy()

        # Number of proposals
        num_proposals = len(cdf)

        # Loop through each row in current data frame creating string
        prop_str = ""
        if num_proposals > 0:
            for idx, row in cdf.iterrows():
                if idx == 0:
                    prop_str += f"{row['w0']}-{row['h0']}-{row['w']}-{row['h']}"
                else:
                    prop_str += f":{row['w0']}-{row['h0']}-{row['w']}-{row['h']}"

        # Return proposals and number of proposal list
        return [num_proposals, prop_str]
