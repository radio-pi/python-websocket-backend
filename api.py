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


class StreamUrlListResource(Resource):
    def render_GET(self, request):
        streamlist = [{'name': 'Hardbase',         'url': 'http://listen.hardbase.fm/tunein-mp3-pls',   'orderid': 1},
                      {'name': 'Technobase',       'url': 'http://listen.technobase.fm/tunein-mp3-asx', 'orderid': 2},
                      {'name': 'Radio 24',         'url': 'http://icecast.radio24.ch/radio24',          'orderid': 0},
                      {'name': 'Radio SRF 1',      'url': 'http://stream.srg-ssr.ch/m/drs1/mp3_128',    'orderid': 3},
                      {'name': 'Radio SRF 2',      'url': 'http://stream.srg-ssr.ch/m/drs2/mp3_128',    'orderid': 4},
                      {'name': 'Radio SRF 3',      'url': 'http://stream.srg-ssr.ch/m/drs3/mp3_128',    'orderid': 5},
                      {'name': 'Radio Swiss Jazz', 'url': 'http://stream.srg-ssr.ch/m/rsj/mp3_128',     'orderid': 6},
                      {'name': 'Radio Swiss Pop',  'url': 'http://stream.srg-ssr.ch/m/rsp/mp3_128',     'orderid': 7}]

        return json.dumps(streamlist).encode('utf8')

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
