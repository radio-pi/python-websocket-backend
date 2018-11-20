from twisted.trial import unittest

from radiopi import api

from http_helpers import DummyRequest

class CaptchaResourceTests(unittest.TestCase):
    """Test for :class:`farfetchd.server.CaptchaResource`."""

    def setUp(self):
        self.root = api.VolumeResource()

    def test_IndexResource_render_GET(self):
        """renderGet() should return the index page."""
        request = DummyRequest(['/'])
        request.method = b'GET'
        page = self.root.render_GET(request)
        print(page)
        self.assertIn(b"{\"volume\":", page)
