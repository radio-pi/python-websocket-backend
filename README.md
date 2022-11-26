Radio PI backend
================

A simple REST & websocket server to expose a simple API
to control a music player. Used by a [web client]( https://github.com/radio-pi/python-websocket-backend/blob/master/index.html)
and an [Android APP]( https://github.com/radio-pi/RadioPi ).

# Production

Please check out these two tutorials:

  * [General setup]( https://radio-pi.github.io/2016-01-12-setup-a-radio-pi/  )
  * [Software setup]( https://radio-pi.github.io/2016-01-13-setup-a-radio-pi-software/ )


# Development

It's recommended to use virtualenv!

Install dependencies with:

```
pip install -r requirements.txt
pip install -e .
```
Run with:

```
uvicorn radiopi.main:app --reload
```

Checkout the simple web client at [http://localhost:8000](http://localhost:8000)!


# Testing

To run the test suite you need `tox`.

```
tox -e py310
```

### curl

Here are some useful `curl` commands to copy and paste:


Play a stream or a file:
```
curl -H "Content-Type: application/json" -d '{"url":"http://fritz.de/livemp3"}' http://localhost:8000/play
```


Set volume to 100:
```
curl -H "Content-Type: application/json" -d '{"volume":"100"}' http://localhost:8000/volume
```

Stop the stream:
```
curl -H "Content-Type: application/json" -X POST http://localhost:8000/stop
```
