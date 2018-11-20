Radio PI backend
==================


A simple REST & websocket server to expose a simple API
to control a music player. Used by a [web client]( https://github.com/radio-pi/python-websocket-backend/blob/master/index.html) 
and an [Android APP]( https://github.com/radio-pi/RadioPi ).

# Production

Please check out these two blog posts:

  * [General setup]( https://radio-pi.github.io/2016-01-12-setup-a-radio-pi/  )
  * [Software setup]( https://radio-pi.github.io/2016-01-13-setup-a-radio-pi-software/ )


# Development

It's recommended to use virtualenv!

Install dependencies with:

``` 
pip install -r requirements.txt
``` 
Run with:

```
twistd -ny service.tac
```

Checkout the simple web client at [http://localhost:3000/index](http://localhost:3000/index)!


# Testing

To run the test suite you need `tox`. 

```
tox -e py37
```

### curl

Here are some useful `curl` commands to copy and paste:


Play a stream or a file:

```
# curl
curl -H "Content-Type: application/json" -d '{"url":"http://fritz.de/livemp3"}' http://localhost:3000/play
```


Set volume to 100:

```
curl -H "Content-Type: application/json" -d '{"volume":"100"}' http://localhost:3000/volume
```
