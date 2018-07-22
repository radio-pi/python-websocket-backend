# import the different backends
from backend.IPlayerInterface import IPlayer
import backend.VLCPlayer

# load/configure one backend and check the player
PLAYER = backend.VLCPlayer.Player()
if not isinstance(PLAYER, IPlayer): raise Exception('Bad interface')
if not IPlayer.version() == '1.0': raise Exception('Bad revision')