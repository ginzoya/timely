"""
Main module where most of the work gets done.
"""

import os
import pylast

KEY_PATH = os.getenv("LAST_FM_KEY", None)
SECRET_PATH = os.getenv("LAST_FM_SECRET", None)
USERNAME_PATH = os.getenv("LAST_FM_USER", None)
PW_PATH = os.getenv("LAST_FM_PW", None)

KEY = ""
SECRET = ""
USERNAME = ""
PW_HASH = ""

if not KEY_PATH:
    raise Exception("Couldn't find env var LAST_FM_KEY!")
if not SECRET_PATH:
    raise Exception("Couldn't find env var LAST_FM_SECRET!")
if not USERNAME_PATH:
    raise Exception("Couldn't find env var LAST_FM_USERNAME!")
if not PW_PATH:
    raise Exception("Couldn't find env var LAST_FM_PW!")

def _get_path_contents(path):
    with open(path) as f:
        return f.readline()
    raise IOError("Nothing read from {}!".format(path))

try:
    KEY = _get_path_contents(KEY_PATH)
    SECRET = _get_path_contents(SECRET_PATH)
    USERNAME = _get_path_contents(USERNAME_PATH)
    PW_HASH = pylast.md5(_get_path_contents(PW_PATH))
except IOError as ioe:
    print("Error reading environment variable path(s)!")
    print(ioe)

class Timely(object):
    """
    Object used for making the actual calls to the API.
    """

    def __init__(self):
        self.last_fm = pylast.LastFMNetwork(api_key=KEY,
                                            api_secret=SECRET,
                                            username=USERNAME,
                                            password_hash=PW_HASH)
        self.user = self.last_fm.get_user(USERNAME)

    def get_suggestions(self, **kwargs):
        """
        Returns a list of suggestions (TopItem), sorted by overall score.

        Keyword Arguments
        -----------------
        time_frame : (str, int)
            A tuple of the type (ie. 'days', 'weeks', etc.), and a number.
        """

        res = []

        time_frame = kwargs.get('time_frame', pylast.PERIOD_3MONTHS)

        res = self.user.get_top_albums(period=time_frame,
                                       limit=10)
        album_dict = {}
        # figure out album lengths of each album
        for album in res:
            album_len = self.get_album_length(album.item)
            album_dict[album.item.get_name()] = album_len

        # TODO: filter out albums over the time limit

        return res

    def get_album_length(self, album):
        """
        Returns the length of the album in minutes.

        Parameters
        ----------
        album : pylast.Album

        Returns
        -------
        int
            The number of minutes the album is.
        """
        minutes = 0
        tracks = album.get_tracks()
        # this is really slow, I'll probably need to write my own call
        # to get album duration
        for track in tracks:
            # track duration comes in ms
            minutes += (track.get_duration() / 1000)  # int division
            print(track.get_name() + ": " + str(minutes))
        return minutes


if __name__ == "__main__":
    # this is a bad idea, but let's put all the test code here for now
    timely = Timely()
    suggestions = timely.get_suggestions(time_frame=pylast.PERIOD_1MONTH)

    for suggestion in suggestions:
        print(suggestion)
