import tornado.web as web

class BaseHandler(web.RequestHandler):
    def initialize(self):
        self.mc = self.application.mc
        self.cache = self.application.cache
        self.log = self.application.log
        self.httpc = self.application.httpc

    def get_current_user(self):
        return self.get_secure_cookie("user")