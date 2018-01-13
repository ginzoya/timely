"""
Test driver for LastFm object.
"""

import unittest
import pylast

from timely.timely import Timely

class TestLastFm(unittest.TestCase):
    """
    Unit tests for wrapper.
    """
    def __init__(self):
        self.timely = Timely()
        super().__init__()

    def test_get_album_length(self):
        """
        Make sure album length returns an actual value.
        """
        # get pylast.Album object
        album_dur = self.timely.get_album_length("replace me")
        self.assertGreater(album_dur, 0)

if __name__ == "__main__":
    unittest.main()
