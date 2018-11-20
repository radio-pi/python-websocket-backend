# import the different backends
from radiopi.backend import IPlayerInterface, VLCPlayer

# load/configure one backend and check the player
PLAYER = VLCPlayer.Player()
if not isinstance(PLAYER, IPlayerInterface.IPlayer): raise Exception('Bad interface')
if not IPlayerInterface.IPlayer.version() == '1.0': raise Exception('Bad revision')