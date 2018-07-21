from .IPlayerInterface import IPlayer
import vlc

class Player(IPlayer):

    def __init__(self):
        self.instance = vlc.Instance("--no-xlib")
        self.player = self.instance.media_player_new()
        self.sleep_timer = 0

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
        self.sleep_timer = timeInMinutes

    def get_sleep_timer(self):
        return self.sleep_timer
