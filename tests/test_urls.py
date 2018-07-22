
#root.putChild(b"stop", api.StopResource())
#root.putChild(b"volume", api.VolumeResource())
#root.putChild(b"sleeptimer", sleep_timer)
#root.putChild(b"streamurls", api.StreamUrlListResource())
from radiopi import api

def test_play():
    play = api.PlayResource()
    #play.render_POST('{"url": "teststream"}')
    assert 5 == 5