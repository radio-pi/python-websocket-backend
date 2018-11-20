from twisted.trial import unittest

import json
from io import BytesIO

from radiopi import api

from http_helpers import DummyRequest

class VolumeResourceTests(unittest.TestCase):
    """Test for :class:`api.VolumeResource`."""

    def setUp(self):
        self.root = api.VolumeResource()

    def test_get_and_set_VolumeResource(self):
        # Given
        data = b'{"volume":100}'

        requestPOST = DummyRequest(['/'])
        requestPOST.method = b'POST'
        requestPOST.writeContentBytes(data)

        requestGET = DummyRequest(['/'])
        requestGET.method = b'GET'
        
        # When
        post_page = self.root.render_POST(requestPOST)
        get_page = self.root.render_GET(requestGET)

        # Then
        assert post_page == b"{}"
        assert get_page == data


class SleepTimerResourceTests(unittest.TestCase):
    """Test for :class:`api.SleepTimerResource`."""

    def setUp(self):
        self.root = api.SleepTimerResource()

    def test_get_and_set_SleepTimerResource(self):
        # Given
        data = b'{"time":2}'
        dataExpected = b'{"sleeptimer":1}'

        requestPOST = DummyRequest(['/'])
        requestPOST.method = b'POST'
        requestPOST.writeContentBytes(data)

        requestGET = DummyRequest(['/'])
        requestGET.method = b'GET'
        
        # When
        post_page = self.root.render_POST(requestPOST)
        get_page = self.root.render_GET(requestGET)

        # Then
        assert post_page == b"{}"
        assert get_page == dataExpected
        
        # quit timer thread
        self.root.cancel()


class PlayResourceTests(unittest.TestCase):
    """Test for :class:`api.PlayResource`."""

    def setUp(self):
        self.root = api.PlayResource()

    def test_set_play(self):
        # Given
        data = b'{"url":"https://some.url"}' 

        requestPOST = DummyRequest(['/'])
        requestPOST.method = b'POST'
        requestPOST.writeContentBytes(data)
        
        # When
        post_page = self.root.render_POST(requestPOST)

        # Then
        assert post_page == b"{}"


class StopResourceTests(unittest.TestCase):
    """Test for :class:`api.StopResource`."""

    def setUp(self):
        self.root = api.StopResource()

    def test_set_play(self):
        # Given
        requestPOST = DummyRequest(['/'])
        requestPOST.method = b'POST'
        
        # When
        post_page = self.root.render_POST(requestPOST)

        # Then
        assert post_page == b"{}"
