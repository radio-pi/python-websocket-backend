# You can run this .tap file directly with:
#    twistd -ny service.tac

from twisted.application import service, internet
from twisted.web.server import Site
from twisted.web.resource import Resource
from autobahn.twisted.websocket import WebSocketServerFactory
import api

rpi_service = service.MultiService()

factory = WebSocketServerFactory("ws://localhost:9000", debug=False)
factory.protocol = api.MpdProtocol
# factory.setProtocolOptions(maxConnections=2)

root = Resource()
root.putChild("play", api.PlayResource())
root.putChild("stop", api.StopResource())
root.putChild("volume", api.VolumeResource())
site = Site(root)

internet.TCPServer(3000, site).setServiceParent(rpi_service)
internet.TCPServer(9000, factory).setServiceParent(rpi_service)

application = service.Application("Radio Pi")
# attach the service to its parent application
rpi_service.setServiceParent(application)
