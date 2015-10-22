# coding: utf-8

"""
Websocket application for flask-sockets inspired by gevent-websocket and tornado
"""
import logging
import uuid

import gevent
from geventwebsocket import WebSocketError
from geventwebsocket.gunicorn.workers import GeventWebSocketWorker
from geventwebsocket.protocols.base import BaseProtocol


OPCODE_PING = 0x9


class WebSocketApplication(object):
    protocol_class = BaseProtocol

    def __init__(self):
        self.id = str(uuid.uuid4())
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

    def ping(self, message="ping"):
        self.write_frame(message, OPCODE_PING)

    def close(self):
        self.ws.close()

    @classmethod
    def protocol_name(cls):
        return cls.protocol_class.PROTOCOL_NAME


class WebSocketClient(object):
    protocol_class = BaseProtocol

    def __init__(self, ws):
        """
        :type ws: geventwebsocket.websocket.WebSocket
        """
        self.ws = ws
        self.id = str(uuid.uuid4())
        self.protocol = self.protocol_class(self)
        self.thread = None

    def start(self):
        self.thread = gevent.spawn(self.run)

    def run(self):
        self.protocol.on_open()
        while True:
            try:
                message = self.ws.receive()
            except WebSocketError:
                self.protocol.on_close()
                break

            self.protocol.on_message(message)

            gevent.sleep(0)

    def on_open(self, *args, **kwargs):
        pass

    def on_close(self, *args, **kwargs):
        pass

    def on_message(self, message, *args, **kwargs):
        self.write_message(message)

    def write_message(self, message, binary=False):
        # TODO :if a lock is needed here ?
        self.ws.send(message, binary)

    def write_frame(self, message, opcode):
        self.ws.send_frame(message, opcode)

    def close(self):
        self.ws.close()

    @classmethod
    def protocol_name(cls):
        return cls.protocol_class.PROTOCOL_NAME


class ApplicationManager(object):

    def __init__(self):
        self.clients = set()

    def start(self):
        gevent.spawn(self.run)
        logging.info("manager started")

    def run(self):
        while True:
            gevent.sleep(10)
            to_remove = [client for client in self.clients if client.thread.ready()]
            logging.debug(to_remove)
            [self.clients.remove(client) for client in to_remove]

    def register(self, ws):
        client = WebSocketClient(ws)
        self.clients.add(client)
        client.run()


class WSWorker(GeventWebSocketWorker):
    manager = ApplicationManager()

    def __init__(self, *args, **kwargs):
        super(WSWorker, self).__init__(*args, **kwargs)
        self.manager.start()