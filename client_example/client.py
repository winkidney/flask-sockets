#!/usr/bin/env python
# coding=utf-8
from threading import Thread
from time import sleep
from ws4py.client.threadedclient import WebSocketClient
# from ws4py.client.tornadoclient import TornadoWebSocketClient as WebSocketClient
# from ws4py.client.geventclient import WebSocketClient

HOST = "ws://127.0.0.1:9000/echo3"


class EchoClient(WebSocketClient):

    def __init__(self, url, client_id, *args):
        super(EchoClient, self).__init__(url, *args)
        self.id = client_id

    def opened(self):
        print("connetcion %s opend!" % self.id)

    def closed(self, code, reason):
        print(("Closed down", code, reason))

    def received_message(self, m):
        print("Got turn back message: %s" % m)
        if len(m) == 175:
            self.close(reason='bye bye')

def run(cid):
    client = EchoClient(HOST, cid)
    client.connect()
    client.send("hello1")
    client.send("hello2")
    while True:
        sleep(10)

def multi_run():
    threads = [Thread(target=run, args=(x, )) for x in range(20)]
    for thread in threads:
        thread.setDaemon(True)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    multi_run()
