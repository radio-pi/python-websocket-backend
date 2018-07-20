import json
import player

from twisted.web.resource import Resource

class PlayResource(Resource):
    def render_POST(self, request):
        content = request.content.getvalue().decode('utf8')
        data = json.loads(content)
        if 'url' in data:
            player.PLAYER.play(data['url'])
        return b''


class StopResource(Resource):
    def render_POST(self, request):
        player.PLAYER.stop()
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

            player.PLAYER.set_volume(vol)

        return b'{}'

    def render_GET(self, request):
        vol = player.PLAYER.get_volume()

        # transform volume
        # 60 -> 0
        # 90 -> 100
        vol = int((int(vol) - 60) / 0.3)

        return b'{"volume":' + str(vol)  + ' }'
