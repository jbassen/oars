# Copyright (c) 2017 Jonathan Bassen, Stanford University

from collections import defaultdict
import tornado.gen as gen
import tornado.web as web
import urllib.parse as parse

from path import url_unescape_path
from path import check_path
from base import BaseHandler
from cache import update_bktf_states

class ObjectiveHandler(BaseHandler):
    @web.authenticated
    @gen.coroutine
    def get(self,
    platform, course_name, mapping_name, module_name, objective_name):

        yield update_bktf_states(self.mc, self.cache)

        path = url_unescape_path(\
            username=self.current_user,
            platform=platform,
            course_name=parse.unquote(course_name),
            mapping_name=mapping_name,
            module_name=module_name,
            objective_name=objective_name,
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

        if not check_path(self.cache, path) == 'objective':
            raise web.HTTPError(404)

        skill_names = [
            sn for sn in self.cache['course_maps']\
            [platform][course_name][mapping_name]['o_to_s'].get(objective_name, {})
        ]

        skill_states = {}
        mapping_states = self.cache['bktf_states'][platform][course_name]\
        [mapping_name]
        n_learners = len(mapping_states)
        for skill_name in skill_names:
            n_problems = 0
            for platform_uid in mapping_states:
                if (not self.cache['course_enrollments'][platform][course_name].get(platform_uid)):
                    continue
                n_attempts = mapping_states[platform_uid]['skills'][skill_name]['n_attempts']
                n_problems = max(n_problems, n_attempts)
            skill_states[skill_name] = {}
            skill_states[skill_name]['learned'] = []
            skill_states[skill_name]['unlearned'] = []
            skill_states[skill_name]['learned_attempts'] = [0 for x in range(n_problems+1)]
            skill_states[skill_name]['unlearned_attempts'] = [0 for x in range(n_problems+1)]

            for platform_uid in mapping_states:
                if (not self.cache['course_enrollments'][platform][course_name].get(platform_uid)):
                    continue
                p_learn = mapping_states[platform_uid]['skills'][skill_name]['p_learn']
                n_attempts = mapping_states[platform_uid]['skills'][skill_name]['n_attempts']
                if p_learn >= .9 and n_attempts >= 3:
                    skill_states[skill_name]['learned'].append(platform_uid)
                    skill_states[skill_name]['learned_attempts'][n_attempts] \
                    += 1
                else:
                    skill_states[skill_name]['unlearned'].append(platform_uid)
                    skill_states[skill_name]['unlearned_attempts'][n_attempts] \
                    += 1

        objective_title = self.cache['course_maps'][platform][course_name]\
        [mapping_name]['objective_to_t'][objective_name]

        skill_to_t = self.cache['course_maps'][platform][course_name]\
        [mapping_name]['skill_to_t']

        self.render(\
            'template.html',
            page_data = {
                'platform': platform,
                'course_name': course_name,
                'mapping_name': mapping_name,
                'module_name': module_name,
                'objective_name': objective_name,
                'objective_title': objective_title,
                'skill_names': skill_names,
                'skill_states': skill_states,
                'n_learners': n_learners,
                'skill_to_t': skill_to_t,
            },
            page_script = 'objective',
        )
