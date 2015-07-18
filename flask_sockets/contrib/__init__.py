# coding: utf-8

"""
Websocket application for flask-sockets inspired by gevent-websocket and tornado
"""
from geventwebsocket import WebSocketError
from geventwebsocket.protocols.base import BaseProtocol


class WebSocketApplication(object):
    protocol_class = BaseProtocol

    def __init__(self):
        self.protocol = self.protocol_class(self)

    def __call__(self, ws):
        """
        :type ws: geventwebsocket.websocket.WebSocket
        """
        self.ws = ws
        self.protocol.on_open()

        while True:
            try:
                message = self.ws.receive()
            except WebSocketError:
                self.protocol.on_close()
                break

            self.protocol.on_message(message)

    def on_open(self, *args, **kwargs):
        pass

    def on_close(self, *args, **kwargs):
        pass

    def on_message(self, message, *args, **kwargs):
        self.write_message(message)

    def write_message(self, message, binary=False):
        self.ws.send(message, binary)

    def write_frame(self, message, opcode):
        self.ws.send_frame(message, opcode)

    def close(self):
        self.ws.close()

    @classmethod
    def protocol_name(cls):
        return cls.protocol_class.PROTOCOL_NAME