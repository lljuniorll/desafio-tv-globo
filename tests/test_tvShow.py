from unittest import TestCase
from controller import TvShow


class TestTvShow(TestCase):

    def test_qualify_video_by_duration_valid(self):
        duration = '00:00:50;10'
        result = TvShow.qualify_video_by_duration(duration)
        self.assertTrue(result, 'Deu erro!')

    def test_qualify_video_by_duration_invalid(self):
        duration = '00:00:20;10'
        result = TvShow.qualify_video_by_duration(duration)
        self.assertFalse(result, 'Deu erro!')
