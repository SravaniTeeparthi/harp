import pdb
import pandas as pd
from harp import fdops
from word2number import w2n


class DetectionData:
    """
    Processes detection data for a single video.
    """

    _df = None

    props = None
    """Dictionary containing detections properties """

    def __init__(self, csv_path):
        """
        Initialize an object detection data instance.

        Parameters
        ----------
        csv_path : str
            Path to csv file containing detection information

        Note
        ----
        It is assumed that the directory containing the detections
        csv file has `properties_session.cv` file. This file should
        contain information about current session.
        """
        # Checking files
        fdops.check_if_file_exists(csv_path)

        # loading detection data as a data frame
        self._df = pd.read_csv(csv_path)

        # Dictionary containing detection properties
        self.props = self._get_properties(csv_path)

    def _get_properties(self, csv_path):
        """
        Creates a dictionary containing properties of detection
        data.

        Parameters
        ----------
        csv_path : str
            Path to csv file containing detection information
        """
        props = {}

        # File properties
        loc, fname, ext = fdops.get_loc_name_ext(csv_path)
        props['loc']    = loc
        props['name']   = fname
        props['ext']    = ext

        # Video properties
        props['W']                     = self._df['W'].unique().item()
        props['H']                     = self._df['H'].unique().item()
        props['FPS']                   = self._df['FPS'].unique().item()
        props['vname']                 = self._get_video_name(fname)
        props['dur'], props['f0_last'] = self._get_last_f0_and_dur(props)

        # Detection properties
        props['ndets']        = len(self._df)
        props['dets_per_sec'] = self._get_dets_per_sec(fname)
        props['f0_min']       = self._df['f0'].min()
        props['f0_max']       = self._df['f0'].max()

        return props

    def _get_video_name(self, fname):
        """ Returns video name by parsing csv file name

        Parameters
        ----------
        fname : str
            Name of csv file having object detections
        """
        csv_name_split = fname.split("_")
        thirty_fps_loc = csv_name_split.index("30fps")
        video_name     = "_".join(csv_name_split[0:thirty_fps_loc+1])
        return video_name

    def _get_dets_per_sec(self, fname):
        """
        Computes number of detections that are used per second
        based on file name of csv file.

        Parameters
        ----------
        fname : str
            Name of csv file having object detections
        """
        fname_split = fname.split("_")

        thirty_fps_loc = fname_split.index("30fps")
        num_det_per_sec_loc = thirty_fps_loc + 1

        num_det_per_sec = w2n.word_to_num(fname_split[num_det_per_sec_loc])
        return num_det_per_sec

    def _get_last_f0_and_dur(self, props):
        """ Returns the last picture order count(POC, f0) and video duration
        of video.

        Parameters
        ----------
        props : Dictionary
        A dictionary containing properties of current detections. This is
        not yet complete.
        """
        # Loading properties_session.csv file
        session_csv = f"{props['loc']}/properties_session.csv"
        fdops.check_if_file_exists(session_csv)
        spdf = pd.read_csv(session_csv)

        # Getting properties of video under consideration
        cur_vid_props = spdf[spdf['name'] == props['vname']]

        # Calcuating last frame
        f0_last = int(cur_vid_props['dur'])*int(cur_vid_props['FPS'])
        return cur_vid_props['dur'].item(), f0_last
