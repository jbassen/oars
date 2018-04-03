# Copyright (c) 2017 Jonathan Bassen, Stanford University

import tornado.escape as escape
import tornado.web as web

from base import BaseHandler
from path import url_unescape_path
from path import check_path

class LandingHandler(BaseHandler):

    @web.authenticated
    def get(self, platform):
        path = url_unescape_path(\
            username=self.current_user,
            platform=platform,
            course_name='',
            mapping_name='',
            module_name='',
            objective_name='',
            skill_name='',
            activity_name='',
        )

        if not check_path(self.cache, path) == 'platform':
            raise web.HTTPError(404)

        username = escape.xhtml_escape(self.current_user)
        self.render(\
            'template.html',
            page_data = {
                'platform': platform,
                'course_names': self.cache['ownerships'][platform][username],
            },
            page_script = 'landing',
        )
