# Copyright (c) 2017 Jonathan Bassen, Stanford University

from collections import defaultdict
import tornado.gen as gen
import tornado.web as web
import urllib.parse as parse

from path import url_unescape_path
from path import check_path
from base import BaseHandler
from cache import update_bktf_states

class SkillHandler(BaseHandler):
    @web.authenticated
    @gen.coroutine
    def get(self, platform, course_name,
    mapping_name, module_name, objective_name, skill_name):

        yield update_bktf_states(self.mc, self.cache)

        path = url_unescape_path(\
            username=self.current_user,
            platform=platform,
            course_name=parse.unquote(course_name),
            mapping_name=mapping_name,
            module_name=module_name,
            objective_name=objective_name,
            skill_name=skill_name,
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

        if not check_path(self.cache, path) == 'skill':
            raise web.HTTPError(404)

        activities_data = {
            an: {
                'text': self.cache['course_maps']\
                [platform][course_name][mapping_name]['activity_to_t'][an],
                'attempted': 0,
                'unattempted': 0,
                'first_correct': 0,
                'last_correct': 0,
            }
            for an in self.cache['course_maps']\
            [platform][course_name][mapping_name]['s_to_a'].get(skill_name, {})
        }

        mapping_states = self.cache['bktf_states'][platform][course_name]\
        [mapping_name]
        for platform_uid in mapping_states:
            if (not self.cache['course_enrollments'][platform][course_name].get(platform_uid)):
                continue
            for activity_name in activities_data:
                if len(mapping_states[platform_uid]['activities'][activity_name]) == 0:
                    activities_data[activity_name]['unattempted'] += 1
                else:
                    activities_data[activity_name]['attempted'] += 1
                    if mapping_states[platform_uid]['activities'][activity_name][0]>0.6:
                        activities_data[activity_name]['first_correct'] += 1
                    if mapping_states[platform_uid]['activities'][activity_name][-1]>0.6:
                        activities_data[activity_name]['last_correct'] += 1



        module_names = self.cache['course_maps']\
        [platform][course_name][mapping_name]['modules']
        m_to_a_data = {}

        m_to_a = self.cache['course_maps']\
        [platform][course_name][mapping_name]['m_to_a']
        for module_name in m_to_a:
            m_to_a_data[module_name] = []
            for activity_name in m_to_a[module_name]:
                if activity_name in activities_data:
                    m_to_a_data[module_name].append(\
                        activities_data[activity_name]
                    )

        objective_title = self.cache['course_maps'][platform][course_name]\
        [mapping_name]['objective_to_t'][objective_name]

        skill_title = self.cache['course_maps'][platform][course_name]\
        [mapping_name]['skill_to_t'][skill_name]


        self.render(\
            'template.html',
            page_data = {
                'platform': platform,
                'course_name': course_name,
                'mapping_name': mapping_name,
                'module_name': module_name,
                'objective_name': objective_name,
                'objective_title': objective_title,
                'skill_name': skill_name,
                'skill_title': skill_title,
                'module_names': module_names,
                'm_to_a_data': m_to_a_data,
            },
            page_script = 'skill',
        )
