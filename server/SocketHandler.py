#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
from tornado import websocket, gen
import logging

cl = []


class SocketHandler(websocket.WebSocketHandler):
    def on_message(self, message):
        pass

    def data_received(self, chunk):
        pass

    def check_origin(self, origin):
        return True

    def open(self):
        if self not in cl:
            cl.append(self)

    @gen.coroutine
    def on_ping(self, data):
        logger = logging.getLogger(__name__)

    def on_close(self):
        if self in cl:
            cl.remove(self)
