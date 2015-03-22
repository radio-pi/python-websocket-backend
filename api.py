from mpd import MPDClient
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory


class MpdProtocol(WebSocketServerProtocol):

    def __init__(self):
        self.client = MPDClient()

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")
        self.run = True
        self.client.connect("localhost", 6600)
        #self.doPing()

    def doPing(self):
        if self.run:
            print("ping")
            self.sendMessage("Some test")
            reactor.callLater(5, self.doPing)

    def onMessage(self, payload, isBinary):
        if not isBinary:
            message = payload.decode('utf8') 
            print("Text message received: {0}".format(message))
            if message == "mpd_version":
                payload = self.client.mpd_version
                print(self.client.mpd_version)

        # echo back message verbatim
        self.sendMessage(payload)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        self.run = False
        self.client.close()
        self.client.disconnect()


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory("ws://localhost:9000", debug=False)
    factory.protocol = MpdProtocol
    # factory.setProtocolOptions(maxConnections=2)

    reactor.listenTCP(9000, factory)
    reactor.run()
