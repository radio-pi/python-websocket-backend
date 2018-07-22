# You can run this .tap file directly with:
#    twistd -ny service.tac

from twisted.internet import reactor, defer
from twisted.application import service, internet
from twisted.web.server import Site
from twisted.web.static import File
from twisted.web.resource import Resource
from autobahn.twisted.websocket import WebSocketServerFactory

import sys
sys.path.append('.')

import api, websocket

rpi_service = service.MultiService()

factory = WebSocketServerFactory("ws://localhost:9000")
factory.protocol = websocket.MpdProtocol
# factory.setProtocolOptions(maxConnections=2)

sleep_timer = api.SleepTimerResource()

root = Resource()
root.putChild(b"play", api.PlayResource())
root.putChild(b"stop", api.StopResource())
root.putChild(b"volume", api.VolumeResource())
root.putChild(b"sleeptimer", sleep_timer)
root.putChild(b"streamurls", api.StreamUrlListResource())
root.putChild(b"index", File('index.html'))
site = Site(root)

internet.TCPServer(3000, site).setServiceParent(rpi_service)
internet.TCPServer(9000, factory).setServiceParent(rpi_service)

application = service.Application("Radio Pi")
# attach the service to its parent application
rpi_service.setServiceParent(application)

# cancel running sleeptimer
@defer.inlineCallbacks
def graceful_shutdown():
    yield sleep_timer.cancel()

reactor.addSystemEventTrigger('before', 'shutdown', graceful_shutdown)
