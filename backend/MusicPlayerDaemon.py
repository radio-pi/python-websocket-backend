from IPlayerInterface import IPlayer
from mpd import MPDClient, ConnectionError

HOST = 'localhost'
PORT = 6600

class Player(IPlayer):

    def __init__(self):
        mclient = MPDClient()
        mclient.connect(HOST, PORT)
        self.client = mclient

    def play(self, url):
        self.__client_alive()
        self.client.clear()
        self.client.add(url)
        self.client.play()

    def stop(self):
        self.__client_alive()
        self.client.clear()
        self.client.stop()

    def get_volume(self):
        self.__client_alive()
        statusDICT = self.client.status()
        vol = statusDICT.get('volume')
        return vol

    def set_volume(self, volume):
        self.__client_alive()
        self.client.setvol(volume)

    def __client_alive(self):
        try:
            self.client.ping()
        except ConnectionError:
            mclient = MPDClient()
            mclient.connect(HOST, PORT)
            self.client = mclient
