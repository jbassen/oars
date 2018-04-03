# Copyright (c) 2017 Jonathan Bassen, Stanford University

from collections import defaultdict
import tornado.gen as gen
import tornado.web as web
import urllib.parse as parse

from path import url_unescape_path
from path import check_path
from base import BaseHandler
from cache import update_bktf_states

class CourseHandler(BaseHandler):
    @web.authenticated
    @gen.coroutine
    def get(self, platform, course_name):

        yield update_bktf_states(self.mc, self.cache)

        path = url_unescape_path(\
            username=self.current_user,
            platform=platform,
            course_name=parse.unquote(course_name),
            mapping_name='',
            module_name='',
            objective_name='',
            skill_name='',
            activity_name='',
        )

        if not check_path(self.cache, path) == 'course':
            raise web.HTTPError(404)

        mappings_data = {}
        learners = {}

        for mapping_name, mapping_states in self.cache['bktf_states'][platform][course_name].items():
            skills_recorded = {}
            mappings_data[mapping_name] = {
                'mapping_name': mapping_name,
                'skills_data': [],
            }
            mapping = self.cache['course_maps'][platform][course_name][mapping_name]
            for module_name in mapping['modules']:
                self.log.error('module_name')
                if module_name not in mapping['m_to_o']:
                    continue
                for objective_name in mapping['m_to_o'][module_name]:
                    self.log.error('objective_name')
                    if objective_name not in mapping['o_to_s']:
                        continue
                    for skill_name in mapping['o_to_s'][objective_name]:
                        self.log.error('skill_name')
                        skill_state = {}
                        skill_state['mastered'] = []
                        skill_state['unmastered'] = []
                        skill_state['unknown'] = []
                        for platform_uid in mapping_states:
                            if (not self.cache['course_enrollments'][platform][course_name].get(platform_uid)):
                                continue
                            learners[platform_uid] = True
                            p_learn = mapping_states[platform_uid]['skills'][skill_name]['p_learn']
                            n_attempts = mapping_states[platform_uid]['skills'][skill_name]['n_attempts']
                            if p_learn >= .9 and n_attempts >= 3:
                                skill_state['mastered'].append(platform_uid)
                            elif n_attempts >= 3:
                                skill_state['unmastered'].append(platform_uid)
                            else:
                                skill_state['unknown'].append(platform_uid)

                        if len(skill_state['unknown'])/len(learners) <= 0.5\
                        and len(skill_state['unmastered']) / len(skill_state['mastered']) > 0.25\
                        and (not skills_recorded.get(skill_name) ):
                            mappings_data[mapping_name]['skills_data'].append({
                                'mapping_name': mapping_name,
                                'module_name': module_name,
                                'objective_name': objective_name,
                                'skill_name': skill_name,
                                'skill_title': mapping['skill_to_t'][skill_name],
                                'skill_state': skill_state,
                            })
                        skills_recorded[skill_name] = True

            mappings_data[mapping_name]['skills_data'] = mappings_data[mapping_name]['skills_data'][-3:]


        self.render(\
            'template.html',
            page_data = {
                'platform': path['platform'],
                'course_name': path['course_name'],
                'mappings_data': [md for mn, md in mappings_data.items()],
                'n_learners': len(learners),
            },
            page_script = 'course',
        )
