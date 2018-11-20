from twisted.trial import unittest

from radiopi import api

from http_helpers import DummyRequest

class VolumeResourceTests(unittest.TestCase):
    """Test for :class:`api.VolumeResource`."""

    def setUp(self):
        self.root = api.VolumeResource()

    def test_VolumeResource_render_GET(self):
        """renderGet() should return the volume."""
        request = DummyRequest(['/'])
        request.method = b'GET'
        page = self.root.render_GET(request)
        self.assertIn(b"{\"volume\":", page)


class SleepTimerResourceTests(unittest.TestCase):
    """Test for :class:`api.SleepTimerResource`."""

    def setUp(self):
        self.root = api.SleepTimerResource()

    def test_VolumeResource_render_GET(self):
        """renderGet() should return the volume."""
        request = DummyRequest(['/'])
        request.method = b'GET'
        page = self.root.render_GET(request)
        self.assertIn(b"{\"sleeptimer\":", page)
