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

@sockets.app_route('/echo2')
class WSTest(WebSocketApplication):
    def on_message(self, message, *args, **kwargs):
        self.write_message("this is the client message from %s: %s" % (request.remote_addr, message))
```


## Deployment 

```bash
$gunicorn -b :9000 -k flask_sockets.worker flask_ws:app --debug  --log-level info
```
If you want to use your own worker and add more support(for example client manager).
Just write your app like

```python
from flask_sockets.contrib import WSWorker

@sockets.route('/echo3')
def run_manager(ws):
    WSWorker.manager.register(ws)
```

It will launch a client manager and you can customize your code in `WebSocketClient`
and the manager to manage different clients for multi-users. 

Then launch them by:

```bash
$gunicorn -b :9000 -k your_app:WSWroker your_app:app --debug  --log-level info
```


## Thanks
Inspired by:

+ [flask-sockets](https://github.com/kennethreitz/flask-sockets)
+ [gevent-websockets](https://bitbucket.org/Jeffrey/gevent-websocket/)
+ [python-websocket-example](https://github.com/heroku-examples/python-websockets-chat/)




