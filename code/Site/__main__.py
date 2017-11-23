import logging
import os
import ssl
import tornado.escape as escape
import tornado.gen as gen
import tornado.httpclient as httpclient
import tornado.httpserver as httpserver
import tornado.httputil as httputil
import tornado.ioloop as ioloop
import tornado.web as web

from cache import load_cache
from db import get_mongo_client
from logs import get_app_logger
from routes import get_routes


class OarsApp(web.Application):
    def __init__(self, mc, cache, log):
        handlers = get_routes()

        settings = {
            'cookie_secret': os.environ['COOKIE_SECRET'],
            'login_url': '/',
            'template_path': os.environ['TEMPLATE_PATH'],
            'static_path': os.environ['STATIC_PATH'],
            'debug':True,
            "xsrf_cookies": True,
        }

        self.mc = mc
        self.cache = cache
        self.log = log
        self.httpc = httpclient.AsyncHTTPClient()
        web.Application.__init__(self, handlers, **settings)


@gen.coroutine
def load_server():
    # since @gen.coroutine can't decorate __init__, must pass mc + cache
    mc = get_mongo_client()
    cache = yield load_cache(mc)
    log = get_app_logger(os.environ['LOG_PATH'])

    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_ctx.load_cert_chain(os.environ['CERT_FILE'], os.environ['KEY_FILE'])

    http_server = httpserver.HTTPServer(\
        OarsApp(mc, cache, log),
        ssl_options=ssl_ctx,
    )
    http_server.listen( int(os.environ['TORNADO_PORT']) )


if __name__ == "__main__":
    ioloop.IOLoop.current().run_sync(load_server)
    ioloop.IOLoop.current().start()
