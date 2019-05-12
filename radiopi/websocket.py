from autobahn.twisted.websocket import WebSocketServerProtocol
from twisted.internet import reactor

from .player import PLAYER


class MpdProtocol(WebSocketServerProtocol):

    def __init__(self):
        super(MpdProtocol, self).__init__()
        self.old_volume = -1
        self.old_title = ""
        self.old_stream_key = ""

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")
        self.run = True
        
        self.doVolumeLoop()
        self.sendVolume(PLAYER.get_volume())
        
        self.doTitleLoop()
        self.sendTitle(PLAYER.get_title())

        self.doStreamLoop()
        self.sendStreamKey(PLAYER.get_playing_key())

    def doStreamLoop(self):
        if self.run:
            key = PLAYER.get_playing_key()
            if key != self.old_stream_key:
                self.old_stream_key = key
                self.sendStreamKey(key)
            reactor.callLater(2, self.doStreamLoop)

    def sendStreamKey(self, key):
        msg = '{"stream_key": "' + key + '"}'
        self.sendMessage(msg.encode('utf8'))

    def doTitleLoop(self):
        if self.run:
            title = PLAYER.get_title()
            if title != self.old_title:
                self.old_title = title
                self.sendTitle(title)
            reactor.callLater(4, self.doTitleLoop)

    def sendTitle(self, title):
        msg = '{"title": "' + title + '"}'
        self.sendMessage(msg.encode('utf8'))

    def doVolumeLoop(self):
        if self.run:
            vol = PLAYER.get_volume()

            if vol != self.old_volume:
                self.old_volume = vol

                # transform volume
                # 60 -> 0
                # 90 -> 100
                #ret_vol = int((int(vol) - 60) / 0.3)
                self.sendVolume(vol)
            reactor.callLater(0.5, self.doVolumeLoop)

    def sendVolume(self, vol):
        msg = '{"volume": ' + str(vol) + '}'
        self.sendMessage(msg.encode('utf8'))

    def onMessage(self, payload, isBinary):
        if not isBinary:
            message = payload.decode('utf8')
            print("Text message received: {0}".format(message))

        # echo back message verbatim
        # self.sendMessage(payload)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        self.run = False
