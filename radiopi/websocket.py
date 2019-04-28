from autobahn.twisted.websocket import WebSocketServerProtocol
from twisted.internet import reactor

from .player import PLAYER


class MpdProtocol(WebSocketServerProtocol):

    def __init__(self):
        super(MpdProtocol, self).__init__()
        self.old_volume = -1
        self.old_title = ""

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")
        self.run = True
        self.doVolumeLoop()
        self.doTitleLoop()

    def doTitleLoop(self):
        if self.run:
            title = PLAYER.get_title()
            if title != self.old_title:
                self.old_title = title

                msg = '{"title": "' + title + '"}'
                self.sendMessage(msg.encode('utf8'))
            reactor.callLater(4, self.doTitleLoop)

    def doVolumeLoop(self):
        if self.run:
            vol = PLAYER.get_volume()

            if vol != self.old_volume:
                self.old_volume = vol

                # transform volume
                # 60 -> 0
                # 90 -> 100
                ret_vol = int((int(vol) - 60) / 0.3)

                msg = '{"volume": ' + str(ret_vol) + '}'
                self.sendMessage(msg.encode('utf8'))
            reactor.callLater(0.5, self.doVolumeLoop)

    def onMessage(self, payload, isBinary):
        if not isBinary:
            message = payload.decode('utf8')
            print("Text message received: {0}".format(message))

        # echo back message verbatim
        # self.sendMessage(payload)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        self.run = False
