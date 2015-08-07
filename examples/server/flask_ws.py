from flask import Flask, request
from flask_sockets import Sockets
from flask_sockets.contrib import WebSocketApplication, WSWorker

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


@sockets.route('/echo3')
def run_manager(ws):
    WSWorker.manager.register(ws)