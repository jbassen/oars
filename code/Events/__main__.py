# Copyright (c) 2017 Jonathan Bassen, Stanford University

import logging
import os
import ssl
import tornado.gen as gen
import tornado.httpserver as httpserver
import tornado.ioloop as ioloop
import tornado.web as web

from db import setup_db
from handleEvents import LagunitaEventHandler
from logs import setup_logs


class OarsApp(web.Application):
    def __init__(self, mc):
        handlers = [
            (r'/edx/events', LagunitaEventHandler),
        ]

        settings = {
            'debug':True,
        }

        self.log = setup_logs(os.environ['LOG_PATH'])
        self.mc = mc
        web.Application.__init__(self, handlers, **settings)

@gen.coroutine
def load_server():
    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_ctx.load_cert_chain(os.environ['CERT_FILE'], os.environ['KEY_FILE'])

    # since @gen.coroutine can't decorate __init__, must pass db_setup + cache
    mc = setup_db()

    http_server = httpserver.HTTPServer(\
        OarsApp(\
            mc,
        ),
        ssl_options=ssl_ctx,
    )
    http_server.listen( int(os.environ['TORNADO_PORT']) )

if __name__ == "__main__":
    ioloop.IOLoop.current().run_sync(load_server)
    ioloop.IOLoop.current().start()
