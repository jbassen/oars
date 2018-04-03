# Copyright (c) 2017 Jonathan Bassen, Stanford University

from collections import defaultdict
import datetime
import tornado.gen as gen


@gen.coroutine
def load_cache(mc):
    cache = init_cache()
    yield load_course_data(mc, cache)
    load_skill_params(cache)
    yield load_enrollments(mc, cache)
    return cache


def init_cache():
    cache = {}

    cache['enrollments_insertstamp'] = datetime.datetime(1,1,1,1,1)
    cache['logs_insertstamp'] = datetime.datetime(1,1,1,1,1)

    # platform>course_name>mapping_name>course_map
    cache['course_data']\
    = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {})))

    # currently saved in code
    cache['skill_params']\
    = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {}))))

    # platform>course_name>mapping_name>platform_uid
    cache['state']\
    = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {}))))

    return cache


@gen.coroutine
def load_course_data(mc, cache):
    core_course_maps = mc.core.course_maps
    course_map_cursor = core_course_maps.find()
    while(yield course_map_cursor.fetch_next):
        course_map = course_map_cursor.next_object()
        platform = course_map['platform']
        course_name = course_map['course_name']
        mapping_name = course_map['mapping_name']

        cache['course_data'][platform][course_name][mapping_name] = course_map
        cache['state'][platform][course_name][mapping_name] = defaultdict(lambda: {})


def load_skill_params(cache):
    for platform, platform_data in cache['course_data'].items():
        platform_params = cache['skill_params'][platform]
        for course_name, course_data in platform_data.items():
            course_params = platform_params[course_name]
            for mapping_name, mapping_data in course_data.items():
                mapping_params = course_params[mapping_name]
                for skill_name in mapping_data['skills']:
                    mapping_params[skill_name] = {
                        'p_init': 0.5,
                        'p_trans': 0.2,
                        'p_guess': 0.2,
                        'p_slip': 0.2,
                    }


@gen.coroutine
def load_enrollments(mc, cache):
    core_enrollments = mc.core.enrollments
    for platform, platform_data in cache['course_data'].items():
        for course_name, course_data in platform_data.items():
            enrollments_cursor = core_enrollments.find({
                'course_name': course_name,
                'platform': platform,
            })
            while(yield enrollments_cursor.fetch_next):
                enrollment = enrollments_cursor.next_object()
                platform_uid = enrollment['platform_uid']
                cache_enrollment(platform_uid, platform, course_name, cache)
                update_enrollments_insertstamp(cache, enrollment['insertstamp'])


def cache_enrollment(platform_uid, platform, course_name, cache):
    course_data = cache['course_data'][platform][course_name]
    course_params = cache['skill_params'][platform][course_name]
    course_state = cache['state'][platform][course_name]
    for mapping_name, mapping_data in course_data.items():
        if platform_uid in course_state[mapping_name]:
            continue
        course_state[mapping_name][platform_uid] = {
            'activities': {},
            'skills': {},
            'objectives': {},
            'timestamp': datetime.datetime(1,1,1,1,1),
            'platform_uid': platform_uid,
            'platform': platform,
            'course_name': course_name,
            'mapping_name': mapping_name,
        }
        state = course_state[mapping_name][platform_uid]
        for activity_name in mapping_data['activities']:
            state['activities'][activity_name] = []
        state['skills'] = {}
        for skill_name in mapping_data['skills']:
            state['skills'][skill_name] = {
                'p_learn': course_params[mapping_name][skill_name]['p_init'],
                'n_attempts': 0,
            }
        state['objectives'] = {}
        for objective_name in mapping_data['objectives']:
            state['objectives'][objective_name] = {
                'n_mastered': 0,
                'n_unmastered': len(mapping_data['o_to_s'].get(objective_name, {})),
            }


def update_enrollments_insertstamp(cache, enrollments_insertstamp):
    cache['enrollments_insertstamp']\
    = max(cache['enrollments_insertstamp'], enrollments_insertstamp)


def update_logs_insertstamp(cache, logs_insertstamp):
    cache['logs_insertstamp']\
    = max(cache['logs_insertstamp'], logs_insertstamp)
