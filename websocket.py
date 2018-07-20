from twisted.internet import reactor

from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory

import player

class MpdProtocol(WebSocketServerProtocol):

    def __init__(self):
        super(MpdProtocol, self).__init__()
        self.old_volume = -1

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")
        self.run = True
        self.doLoop()

    def doLoop(self):
        if self.run:
            vol = player.PLAYER.get_volume()

            if vol != self.old_volume:
                self.old_volume = vol
                
                # transform volume
                # 60 -> 0
                # 90 -> 100
                ret_vol = int((int(vol) - 60) / 0.3)

                self.sendMessage("{0}".format(ret_vol).encode('utf8'))
            reactor.callLater(0.5, self.doLoop)

    def onMessage(self, payload, isBinary):
        if not isBinary:
            message = payload.decode('utf8') 
            print("Text message received: {0}".format(message))

        # echo back message verbatim
        self.sendMessage(payload)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        self.run = False