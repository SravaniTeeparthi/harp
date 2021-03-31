import os
import cv2
import pdb
import skvideo.io as skvio
from harp import fdops

class VidReader:
    """ Video reader class
    """
    _v = None

    props = None
    """ Video propoerties """

    def __init__(self, pth):
        """
        Intialize a video instance

        Parameters
        ----------
        pth : str
        Path to full video
        """
        # Check if the video exists
        fdops.check_if_file_exists(pth)

        # Create a opencv video instance
        self._v = cv2.VideoCapture(pth)

        # Compute video properties
        self.props = self._get_video_properties(pth)

    def get_frame(self, frm_num, c='rgb'):
        """
        Returns a frame(RGB) from video using its frame number

        Parameters
        ----------
        frm_num: int
            Frame number
        c : str, default rgb
            String with either of following values, {bgr, rgb}

        """
        # seek to frame
        self._v.set(cv2.CAP_PROP_POS_FRAMES, frm_num)
        _, frame = self._v.read()
        if c == 'bgr':
            return frame
        elif c == 'rgb':
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return frame
        else:
            raise Exception(f"Invalid parameter for corlor\n\t{c}")


    def _get_video_properties(self, pth):
        """ Returns  a dictionary with video properties

        Parameters
        ----------
        pth : str
        Path to full video
        """
        # Get video file name and directory location
        vdir_loc, vname, vext = fdops.get_loc_name_ext(pth)

        # Read video meta information
        vmeta = skvio.ffprobe(pth)

        # If it is empty i.e. scikit video cannot read metadata
        # return empty stings and zeros
        if vmeta == {}:
            vprops = {
                'islocal': False,
                'full_path': pth,
                'name': vname,
                'extension': vext,
                'dir_loc': vdir_loc,
                'frame_rate': 0,
                'duration': 0,
                'num_frames': 0,
                'width': 0,
                'height': 0
            }

            return vprops

        # Calculate average frame rate
        fr_str = vmeta['video']['@avg_frame_rate']
        fr = round(
            int(fr_str.split("/")[0]) / int(fr_str.split("/")[1])
        )

        # get duration
        vdur = round(float(vmeta['video']['@duration']))

        # get number of frames
        vnbfrms = int(vmeta['video']['@nb_frames'])

        # video width
        width = int(vmeta['video']['@width'])

        # video height
        height = int(vmeta['video']['@height'])

        # Creating properties dictionary
        vprops = {
            'islocal': True,
            'full_path': pth,
            'name': vname,
            'extension': vext,
            'dir_loc': vdir_loc,
            'frame_rate': fr,
            'duration': vdur,
            'num_frames': vnbfrms,
            'width': width,
            'height': height
        }

        return vprops

        # File properties
        loc, fname, ext = fdops.get_loc_name_ext(pth)
        props['loc']    = loc
        props['name']   = fname
        props['ext']    = ext

    def release(self):
        """ deletes instance """
        self._v.release()
        del self
