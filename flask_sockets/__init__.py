# -*- coding: utf-8 -*-

def log_request(self):
    log = self.server.log
    if log:
        if hasattr(log, 'info'):
            log.info(self.format_request() + '\n')
        else:
            log.write(self.format_request() + '\n')


# Monkeys are made for freedom.
import gevent
from geventwebsocket.gunicorn.workers import GeventWebSocketWorker as Worker

if 'gevent' in locals():
    # Freedom-Patch logger for Gunicorn.
    if hasattr(gevent, 'pywsgi'):
        gevent.pywsgi.WSGIHandler.log_request = log_request



class SocketMiddleware(object):

    def __init__(self, wsgi_app, app, socket):
        self.ws = socket
        self.wsgi_app = wsgi_app
        self.app = app

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        if path in self.ws.url_map:
            handler = self.ws.url_map[path]
            environment_ws = environ.get('wsgi.websocket')

            with self.app.app_context():
                with self.app.request_context(environ):
                    handler(environment_ws)
                    return []
        else:
            return self.wsgi_app(environ, start_response)


class Sockets(object):

    def __init__(self, app=None):
        self.url_map = {}
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.wsgi_app = SocketMiddleware(app.wsgi_app, app, self)

    def route(self, rule, **options):

        def decorator(f):
            endpoint = options.pop('endpoint', None)
            self.add_url_rule(rule, endpoint, f, **options)
            return f
        return decorator

    def add_url_rule(self, rule, _, f, **options):
        self.url_map[rule] = f

    def app_route(self, rule, **options):
        """
        Flask style route decorator.
        Register a websocket class-style view.
        Given class will be instanced and `__call__` will be called
        when websocket connection created.
        """

        def decorator(cls):
            endpoint = options.pop('endpoint', None)

            def get_instance(ws):
                return cls()(ws)
            self.add_url_rule(rule, endpoint, get_instance, **options)
            return cls
        return decorator

# CLI sugar.
if 'Worker' in locals():
    worker = Worker