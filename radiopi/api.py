import json

from twisted.web.resource import Resource

from .player import PLAYER


class CorsResource(Resource):
    """
    Default empty OPTIONS route for
    preflight CORS.
    https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request
    """
    def render_OPTIONS(self, request):
        return b''


class PlayResource(CorsResource):
    def render_POST(self, request):
        content = request.content.getvalue().decode('utf8')
        data = json.loads(content)
        if 'url' in data:
            PLAYER.play(data['url'])
        return b'{}'


class StopResource(CorsResource):
    def render_POST(self, request):
        PLAYER.stop()
        return b'{}'


class SleepTimerResource(CorsResource):
    def render_GET(self, request):
        timeinminutes = PLAYER.get_sleep_timer()
        return ('{"sleeptimer":' + str(timeinminutes) + '}').encode('utf8')

    def render_POST(self, request):
        content = request.content.getvalue().decode('utf8')
        data = json.loads(content)

        if 'time' in data:
            timeinminutes = data['time']
            PLAYER.set_sleep_timer(timeinminutes)
        return b'{}'

    def cancel(self):
        PLAYER.set_sleep_timer(0)


class StreamUrlListResource(CorsResource):
    def render_GET(self, request):
        streamlist = [{
                        'name': 'Hardbase',
                        'url': 'http://listen.hardbase.fm/tunein-mp3-pls',
                        'img': '/image/Hardbasefm.jpg',
                        'orderid': 1
                      },
                      {
                        'name': 'Technobase',
                        'url': 'http://listen.technobase.fm/tunein-mp3-asx',
                        'img': '',
                        'orderid': 2
                      },
                      {
                        'name': 'Radio 24',
                        'url': 'http://icecast.radio24.ch/radio24',
                        'img': 'https://upload.wikimedia.org/wikipedia/de/thumb/3/33/Radio_24_Logo.svg/154px-Radio_24_Logo.svg.png',
                        'orderid': 0
                       },
                      {
                        'name': 'Radio SRF 1',
                        'url': 'http://stream.srg-ssr.ch/m/drs1/mp3_128',
                        'img': 'https://www.srf.ch/play/v3/svgs/radio-srf-1-small.svg',
                        'orderid': 3
                      },
                      {
                        'name': 'Radio SRF 2',
                        'url': 'http://stream.srg-ssr.ch/m/drs2/mp3_128',
                        'img': 'https://www.srf.ch/play/v3/svgs/radio-srf-2-kultur-small.svg',
                        'orderid': 4
                      },
                      {
                        'name': 'Radio SRF 3',
                        'url': 'http://stream.srg-ssr.ch/m/drs3/mp3_128',
                        'img': 'https://www.srf.ch//play/v3/svgs/radio-srf-3-small.svg',
                        'orderid': 5},
                      {
                        'name': 'Radio Swiss Jazz',
                        'url': 'http://stream.srg-ssr.ch/m/rsj/mp3_128',
                        'img': '',
                        'orderid': 6},
                      {
                        'name': 'Radio Swiss Pop',
                        'url': 'http://stream.srg-ssr.ch/m/rsp/mp3_128',
                        'img': '',
                        'orderid': 7
                      }]

        return json.dumps(streamlist).encode('utf8')


class VolumeResource(CorsResource):
    def render_POST(self, request):
        vol = -1
        content = request.content.getvalue().decode('utf8')
        data = json.loads(content)

        if 'volume' in data:
            # transform volume
            # 000 -> 60
            # 100 -> 90
            vol = data['volume']
            #vol = int((float(vol) * 0.3) + 60)

            PLAYER.set_volume(vol)

        return b'{}'

    def render_GET(self, request):
        vol = PLAYER.get_volume()

        # transform volume
        # 60 -> 0
        # 90 -> 100
        #vol = int((int(vol) - 60) / 0.3)

        return ('{"volume":' + str(vol) + '}').encode('utf8')
