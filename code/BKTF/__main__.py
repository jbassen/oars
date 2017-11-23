import logging
import time
import tornado.gen as gen
import tornado.ioloop as ioloop

from cache import cache_enrollment
from cache import load_cache
from cache import update_logs_insertstamp
from cache import update_enrollments_insertstamp
from db import get_enrollments_updates
from db import get_logs_updates
from db import get_mongo_client
from db import upsert_states
from db import upsert_state


@gen.coroutine
def main():
    mc = get_mongo_client()
    #load data to cache
    cache = yield load_cache(mc)
    yield upsert_states(mc, cache)
    while(True):
        yield handle_enrollments_updates(mc, cache)
        n_logs_updates = yield handle_logs_updates(mc, cache)
        if not n_logs_updates:
            time.sleep(10)


@gen.coroutine
def handle_enrollments_updates(mc, cache):
    enrollments_collection = get_enrollments_updates(\
        mc,
        cache['enrollments_insertstamp'],
    )
    while(yield enrollments_collection.fetch_next):
        enrollment = enrollments_collection.next_object()
        platform_uid = enrollment['platform_uid']
        platform = enrollment['platform']
        course_name = enrollment['course_name']
        enrollments_insertstamp = enrollment['insertstamp']
        cache_enrollment(platform_uid, platform, course_name, cache)
        update_enrollments_insertstamp(cache, enrollments_insertstamp)


@gen.coroutine
def handle_logs_updates(mc, cache):
    logs_collection = get_logs_updates(mc, cache['logs_insertstamp'])
    n_logs_updates = 0
    while(yield logs_collection.fetch_next):
        n_logs_updates += 1
        event = logs_collection.next_object()
        if event['max_grade'] > 0:
            if event['course_name'] in cache['course_data'][event['platform']]:
                yield handle_event(mc, cache, event)
        update_logs_insertstamp(cache, event['insertstamp'])
    return n_logs_updates


@gen.coroutine
def handle_event(mc, cache, event):
    platform = event['platform']
    course_name = event['course_name']
    platform_uid = event['platform_uid']
    activity_name = event['activity_name']
    timestamp = event['timestamp']
    score = event['grade']/event['max_grade']

    course_state = cache['state'][platform][course_name]
    for mapping_name, mapping_state in course_state.items():
        mapping_data = cache['course_data'][platform][course_name][mapping_name]
        if activity_name not in mapping_data['activity_to_t']:
            return
        if platform_uid not in mapping_state:
            cache_enrollment(platform_uid, platform, course_name, cache)
        update_state(cache, platform, course_name, mapping_name,
        platform_uid, activity_name, score, timestamp)
        yield upsert_state(mc, mapping_state[platform_uid])


def update_state(cache, platform, course_name, mapping_name,
platform_uid, activity_name, score, timestamp):
    state = cache['state'][platform][course_name][mapping_name][platform_uid]
    mapping_data = cache['course_data'][platform][course_name][mapping_name]
    mapping_params = cache['skill_params'][platform][course_name][mapping_name]
    state['activities'][activity_name].append(score)
    state['timestamp'] = timestamp
    if len(state['activities'][activity_name]) == 1:
        update_skills_state(state, mapping_data, mapping_params,
        activity_name, score)
        update_objectives_state(state, mapping_data)


def update_skills_state(state, mapping_data, mapping_params,
activity_name, score):
    for skill_name in mapping_data['a_to_s'].get(activity_name, {}):
        params = mapping_params[skill_name]
        skill_state = state['skills'][skill_name]
        score_m1 = score - 1
        p_old = skill_state['p_learn']
        p_old_c = 1 - p_old
        p_slip = params['p_slip']
        p_slip_c = 1 - p_slip
        p_guess = params['p_guess']
        p_guess_c = 1 - p_guess
        p_trans = params['p_trans']

        p_learn = score * p_old * p_slip_c \
        / (p_old * p_slip_c + p_old_c * p_guess) \
        - score_m1 * p_old * p_slip \
        / (p_old * p_slip + p_old_c * p_guess_c)

        skill_state['p_learn'] = p_learn + (1 - p_learn) * p_trans

        skill_state['n_attempts'] += 1


def update_objectives_state(state, mapping_data):
    for objective_name in mapping_data['objectives']:
        n_mastered = 0
        n_unmastered = 0
        for skill_name in mapping_data['o_to_s'].get(objective_name, {}):
            skill_state = state['skills'][skill_name]
            if skill_state['p_learn'] >= 0.9 and skill_state['n_attempts'] >= 3:
                n_mastered += 1
            else:
                n_unmastered += 1
        state['objectives'][objective_name]['n_mastered'] = n_mastered
        state['objectives'][objective_name]['n_unmastered'] = n_unmastered


if __name__ == "__main__":
    ioloop.IOLoop.current().run_sync(main)
