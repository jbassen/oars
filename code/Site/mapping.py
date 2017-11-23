import tornado.gen as gen
import tornado.web as web
import urllib.parse as parse

from path import url_unescape_path
from path import check_path
from base import BaseHandler

class MappingHandler(BaseHandler):
    @web.authenticated
    @gen.coroutine
    def get(self, platform, course_name, mapping_name):

        path = url_unescape_path(\
            username=self.current_user,
            platform=platform,
            course_name=parse.unquote(course_name),
            mapping_name=mapping_name,
            module_name='',
            objective_name='',
            skill_name='',
            activity_name='',
        )

        if not check_path(self.cache, path) == 'mapping':
            raise web.HTTPError(404)

        module_names = [
            mn for mn in self.cache['course_maps']\
            [path['platform']][path['course_name']]\
            [path['mapping_name']]['modules']
        ]

        self.render(\
            'template.html',
            page_data = {
                'platform': path['platform'],
                'course_name': path['course_name'],
                'mapping_name': path['mapping_name'],
                'module_names': module_names,
            },
            page_script = 'mapping',
        )
