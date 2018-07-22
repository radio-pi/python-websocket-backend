Radio PI backend
==================


It's a simple REST & websocket server to expose a simple API
to controll a music player. Used by a [Webclient]( https://github.com/radio-pi/python-websocket-backend/blob/master/index.html) 
and an [Android app]( https://github.com/radio-pi/RadioPi ).

# Production

Please check out these two blog posts:

  * [General setup]( https://radio-pi.github.io/2016-01-12-setup-a-radio-pi/  )
  * [Software setup]( https://radio-pi.github.io/2016-01-13-setup-a-radio-pi-software/ )


# Development

It's recomended to use virtualenv!

Install dependencies with:

``` 
pip install -r requirements.txt
``` 
Run with:

```
twistd -ny service.tac
```

Checkout the simple http client at [http://localhost:3000/index](http://localhost:3000/index)!

Testing with `curl`

```
# curl
curl -H "Content-Type: application/json" -d '{"url":"http://fritz.de/livemp3"}' http://localhost:3000/play
curl -H "Content-Type: application/json" -d '{"volume":"100"}' http://localhost:3000/volume
```
