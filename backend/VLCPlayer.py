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
