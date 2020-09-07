#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
import asyncio
import logging
import os
import signal
import sys
import time
from functools import partial

import tornado.ioloop
import tornado.httpserver
import tornado.web
import tornado.httpclient
import tornado.options
from tornado.log import enable_pretty_logging
from tornado.options import define, options

from server import webservice
from server.MainHandler import MainHandler
from server.SocketHandler import SocketHandler

define("port", default=8080, help="Run on the given port", type=int)

# Constants
_MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 2


def sig_handler(logger, server, sig, frame):
    """
    Signal Handler for Interrupts from Web Server
    Args:
        :param logger:
        :param server:
        :param sig:
        :param frame:
    Returns:
        :return:
    """
    io_loop = tornado.ioloop.IOLoop.instance()

    def stop_loop(deadline):
        """
        Stop the ioloop
        :param deadline:
        :return:
        """
        now = time.time()
        if now < deadline:
            logger.info('Waiting for next tick')
            io_loop.add_timeout(now + 1, stop_loop, deadline)
        else:
            io_loop.stop()
            time.sleep(1)
            logger.info('Shutdown finally')

    def shutdown():
        """
        Shutdown tornado server
        :return:
        """
        logger.info('Stopping http server')
        server.stop()
        logger.info('Will shutdown in %s seconds ...',
                    _MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
        stop_loop(time.time() + _MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)

    logger.warning('Caught signal: {}'.format(sig))
    io_loop.add_callback_from_signal(shutdown)


def make_app():
    """
    Adds application handler to tornado
    Returns:
        :return: tornado web application
    """
    return tornado.web.Application(handlers=[
        (r'/ws', SocketHandler),
        (r".*", MainHandler)], )


def main():
    """
    Starts Tornado Web Server and Waits for any SIG calls
    :return: None
    """
    # For logging tornado application logs
    print("Starting ThirdEye Dummy Server...")
    logger = logging.getLogger("Main")
    f = open(os.devnull, 'w')
    sys.stdout = f
    # To display tornado logs on console.
    enable_pretty_logging()

    logger.setLevel(webservice.log_level)

    logger.info("Starting Third Eye with Tornado Web Service")

    # for accepting commandline args for tornado web server
    tornado.options.parse_command_line()

    logger = logging.getLogger("tornado.application")
    logger.setLevel(webservice.log_level)
    app = make_app()

    http_server = tornado.httpserver.HTTPServer(app, xheaders=True, no_keep_alive=False)
    http_server.listen(options.port)
    logger.info(http_server)

    # Adding SIG calls callback for handling system interrupts and shutdown tornado gracefully
    signal.signal(signal.SIGTERM, partial(sig_handler, logger, http_server))
    signal.signal(signal.SIGINT, partial(sig_handler, logger, http_server))

    # Start Tornado Web Server
    tornado.ioloop.IOLoop.current().start()
    logger.info('Exit...')


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()
