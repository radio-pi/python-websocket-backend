import json

from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource

from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory


# import the different backends
from backend.IPlayerInterface import IPlayer
import backend.VLCPlayer 


# load one backend and check the player
PLAYER = backend.VLCPlayer.Player()
if not isinstance(PLAYER, IPlayer): raise Exception('Bad interface')
if not IPlayer.version() == '1.0': raise Exception('Bad revision')


class PlayResource(Resource):
    def render_POST(self, request):
        content = request.content.getvalue().decode('utf8')
        data = json.loads(content)
        if 'url' in data:
            PLAYER.play(data['url'])
        return b''


class StopResource(Resource):
    def render_POST(self, request):
        PLAYER.stop()
        return b''


class VolumeResource(Resource):
    def render_POST(self, request):
        vol = -1
        content = request.content.getvalue().decode('utf8')
        data = json.loads(content)

        if 'volume' in data:
            # transform volume
            # 000 -> 60
            # 100 -> 90
            vol = data['volume']
            vol = int((float(vol) * 0.3) + 60)

            PLAYER.set_volume(vol)

        return b'{}'

    def render_GET(self, request):
        vol = PLAYER.get_volume()

        # transform volume
        # 60 -> 0
        # 90 -> 100
        vol = int((int(vol) - 60) / 0.3)

        return b'{"volume":' + str(vol)  + ' }'

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
            vol = PLAYER.get_volume()

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
