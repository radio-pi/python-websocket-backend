import re
import struct
import urllib.request as urllib2

import vlc

from .IPlayerInterface import IPlayer
from .sleep import Sleep


class Player(IPlayer):

    def __init__(self):
        self.instance = vlc.Instance("--no-xlib")
        self.player = self.instance.media_player_new()
        self.sleep_timer = None

    def play(self, url):
        media = self.instance.media_new(url)
        self.player.set_media(media)
        self.player.play()

    def stop(self):
        self.player.stop()

    def get_playing_key(self):
        url = ""
        if self.player.get_media():
            url = self.player.get_media().get_mrl()

        return url

    def get_title(self):
        title = ''
        if not self.player.get_media():
            return title

        url = self.player.get_media().get_mrl()

        request = urllib2.Request(url, headers={'Icy-MetaData': 1})
        response = urllib2.urlopen(request)
        metaint = int(response.headers['icy-metaint'])

        for _ in range(200):
            response.read(metaint)
            metadata_length = struct.unpack('B', response.read(1))[0] * 16
            metadata = response.read(metadata_length).rstrip(b'\0')
            metadata = self._decode_metadata(metadata)

            m = re.search(r"StreamTitle='([^']*)';", metadata)
            if m:
                title = m.group(1)
                if title:
                    break
        return title

    def get_volume(self):
        vol = self.player.audio_get_volume()
        return vol

    def set_volume(self, volume):
        self.player.audio_set_volume(volume)

    def set_sleep_timer(self, timeInMinutes):
        """
        Create a new sleep timer. Cancels any existing timers.
        When set to 0 cancles timers.
        """
        if self.sleep_timer:
            self.sleep_timer.cancel()

        if timeInMinutes > 0:
            self.sleep_timer = Sleep(timeInMinutes, self.stop)

    def get_sleep_timer(self):
        if self.sleep_timer:
            return self.sleep_timer.remaining()
        else:
            return 0

    def _decode_metadata(self, metadata):
        try:
            metadata = metadata.decode('utf8')
        except UnicodeDecodeError:
            try:
                metadata = metadata.decode('latin-1')
            except UnicodeDecodeError:
                metadata = metadata.decode('utf8', errors='replace')
        return metadata
