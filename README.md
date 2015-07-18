Flask-Sockets-Tornado
========================

Flask-Sockets Tornado style version.    

The original repo is [here](https://github.com/kennethreitz/flask-sockets).    

Differences:    
+ Tornado-style application-class supoort (`WebSocketHandler`).
+ FLask's request and WSGI context support.
+ Improvement on setup.py(add gevent's version require).
+ Flask demo app included.

## Installation

Run shell command:

```bash
$python setup.py install
```

## Quick Start

```python
from flask import Flask, request
from flask_sockets import Sockets
from flask_sockets.contrib import WebSocketApplication

app = Flask(__name__)
sockets = Sockets(app)

@app.route('/')
def hello_world():
    return 'Hello World!'


@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)

@sockets.app_route('/echo')
class WSTest(WebSocketApplication):
    def on_message(self, message, *args, **kwargs):
        self.ws.send("this is the client message from %s: %s" % (request.remote_addr, message))
```


## Deployment 

```bash
$gunicorn -b :9000 -k flask_sockets.worker flask_ws:app --debug  --log-level info
```

## Thanks
Inspired by:

+ [flask-sockets](https://github.com/kennethreitz/flask-sockets)
+ [gevent-websockets](https://bitbucket.org/Jeffrey/gevent-websocket/)
+ [python-websocket-example](https://github.com/heroku-examples/python-websockets-chat/)




