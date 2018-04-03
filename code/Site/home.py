# Copyright (c) 2017 Jonathan Bassen, Stanford University

import tornado.escape as escape
import tornado.web as web

from base import BaseHandler

class HomeHandler(BaseHandler):

    def get(self):
        self.render(\
            'template.html',
            page_data = {},
            page_script = 'home'
        )
