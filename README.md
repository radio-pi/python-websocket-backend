Radio PI backend
==================

This project replace the old node.js backend. It's the glue 
code which expose the mpd as simple REST API.

# Production

Please check out these two blog posts:

  * [General setup](http://radio-pi.github.io/2015/07/06/setup-a-radio-pi/  )
  * [Software setup] ()


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

Serve the index.html

```
python -m SimpleHTTPServer 8080
```
