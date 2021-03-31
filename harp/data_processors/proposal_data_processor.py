import cv2
import pdb
import skvideo
import numpy as np
import pandas as pd
from tqdm import tqdm
from harp import fdops
from word2number import w2n
from harp.vid import VidReader

class RegPropData:
    """
    Processes region proposal data.
    """

    _df = None

    props = None
    """Dictionary containing region proposal data properties """

    def __init__(self, csv_path):
        """
        Initialize a region proposal data instance.

        Parameters
        ----------
        csv_path : str
            Path to csv file containing proposal information.

        Note
        ----
        It is assumed that the directory containing the proposals
        csv file has `properties_session.cv` file. This file should
        contain information about current session.
        """
        # Checking files
        fdops.check_if_file_exists(csv_path)

        # loading proposal data as a data frame
        self._df = pd.read_csv(csv_path)

        # Dictionary containing proposal properties
        self.props = self._get_properties(csv_path)

    def _get_properties(self, csv_path):
        """
        Creates a dictionary containing properties of proposal
        data.

        Parameters
        ----------
        csv_path : str
            Path to csv file containing proposal information
        """
        props = {}

        # File properties
        loc, fname, ext = fdops.get_loc_name_ext(csv_path)
        props['loc'] = loc
        props['name'] = fname
        props['ext'] = ext

        # Video properties
        props['W'] = self._df['W'].unique().item()
        props['H'] = self._df['H'].unique().item()
        props['FPS'] = self._df['FPS'].unique().item()
        props['dur'] = self._df['dur'].unique().item()
        props['vname'] = self._get_video_name(fname)

        # Proposal properties
        props['num_props'] = self._get_num_proposals()

        return props

    def write_proposals_to_video(self, vdir, frms_per_sec=1.0):
        """ Writes proposals to video.

        Parameters
        ----------
        vdir : str
            Directory where we can find video.
        frms_per_sec : float, default 1
            A value of 0.5 means that we will skip
            `FPS x 1/(frms_per_sec) = 60` frames
        """
        # Input video
        vid_name = self.props['vname']
        vfpath = fdops.get_files_with_kws(vdir, [vid_name, ".mp4"])
        if len(vfpath) > 1:
            raise Exception(f"More than one video found\n\t{vfpath}")
        vin = VidReader(vfpath[0])

        # Output video
        ovid_path = f"{self.props['loc']}/{self.props['name']}.mp4"
        vw = skvideo.io.FFmpegWriter(
            ovid_path,
            outputdict={'-vcodec': 'libx264','-r':'30'}
        )

        # Calculate frame numbers(POC) that we will use.
        f0_start = 0  # starting frame poc
        f0_end = vin.props['num_frames'] - 1  # ending frame poc
        f0_skip = vin.props['frame_rate']*(1/frms_per_sec)
        f0s = list(range(f0_start, f0_end, int(f0_skip)))

        # Loop over each frame number and draw proposal regions
        # over them
        for f0 in tqdm(f0s):
            frm = vin.get_frame(f0, c='bgr')

            # Get proposals for frame f0
            props = self._get_proposals_for_frame(f0)

            # Proposals looop
            for p in props:
                if len(p) > 0:
                    w0, h0, w, h = p
                    frame = cv2.rectangle(
                        frm, (w0, h0), (w0+w, h0+h), (0, 256, 0), 1
                    )
            # Write frame to output
            vw.writeFrame(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        vw.close()
        vin.release()
        import sys; sys.exit()

    def _get_proposals_for_frame(self, fn):
        """
        Returns a list of proposal regions

        Parameters
        ----------
        fn : int
        Frame number
        """

        # Get dataframe that contains f0. It should have only one row
        tdf = self._df.copy()  # lower bound
        tdf['f1'] = (tdf['f0']                      # creating column
                     + tdf['f'] - 1)                # with last frame
        df = tdf[fn >= tdf['f0']]
        df = df[fn <= df['f1']]
        if len(df) == 0:
            return []
        if len(df) > 1:
            pdb.set_trace()
            raise Exception("USER_ERROR: proposals csv is fishy\n"
                            f"{df}")

        # Proposal string to numpy array
        prop_list = df['props'].item().split(":")

        # Loop over bounding box list and create a numpy array
        if len(prop_list) > 0:
            props = []
            for p in prop_list:
                coords = p.split("-")
                if len(coords) == 4:
                    props += [[int(x) for x in coords]]
        return props

    def _get_video_name(self, fname):
        """ Returns video name by parsing csv file name

        Parameters
        ----------
        fname : str
            Name of csv file having proposals
        """
        csv_name_split = fname.split("_")
        thirty_fps_loc = csv_name_split.index("30fps")
        video_name = "_".join(csv_name_split[0:thirty_fps_loc+1])
        return video_name

    def _get_num_proposals(self):
        """ Returns number of proposals.
        """
        total_props = self._df['nprops'].sum()
        return total_props
