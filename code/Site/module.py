from collections import defaultdict
import tornado.gen as gen
import tornado.web as web
import urllib.parse as parse

from path import url_unescape_path
from path import check_path
from base import BaseHandler
from cache import update_bktf_states

class ModuleHandler(BaseHandler):
    @web.authenticated
    @gen.coroutine
    def get(self, platform, course_name, mapping_name, module_name):

        yield update_bktf_states(self.mc, self.cache)

        path = url_unescape_path(\
            username=self.current_user,
            platform=platform,
            course_name=parse.unquote(course_name),
            mapping_name=mapping_name,
            module_name=module_name,
            objective_name='',
            skill_name='',
            activity_name='',
        )

        username = path['username']
        platform = path['platform']
        course_name = path['course_name']
        mapping_name = path['mapping_name']
        module_name = path['module_name']
        objective_name = path['objective_name']
        skill_name = path['skill_name']
        activity_name = path['activity_name']

        if not check_path(self.cache, path) == 'module':
            raise web.HTTPError(404)

        objective_names = [
            on for on in self.cache['course_maps']\
            [platform][course_name][mapping_name]['m_to_o'].get(module_name, {})
        ]

        objective_states = {}
        for objective_name in objective_names:
            objective_states[objective_name] = {}
            objective_states[objective_name]['mastered'] = []
            objective_states[objective_name]['unmastered'] = []

        mapping_states = self.cache['bktf_states'][platform][course_name]\
        [mapping_name]
        for platform_uid in mapping_states:
            if (not self.cache['course_enrollments'][platform][course_name].get(platform_uid)):
                continue
            for objective_name in objective_names:
                if mapping_states[platform_uid]['objectives'][objective_name]\
                ['n_unmastered'] == 0:
                    objective_states[objective_name]['mastered'].append(platform_uid)
                else:
                    objective_states[objective_name]['unmastered'].append(platform_uid)

        objective_to_t = self.cache['course_maps'][platform][course_name]\
        [mapping_name]['objective_to_t']

        self.render(\
            'template.html',
            page_data = {
                'platform': platform,
                'course_name': course_name,
                'mapping_name': mapping_name,
                'module_name': module_name,
                'objective_names': objective_names,
                'objective_states': objective_states,
                'objective_to_t': objective_to_t,
            },
            page_script = 'module',
        )
