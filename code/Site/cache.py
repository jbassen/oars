from collections import defaultdict
import datetime
import tornado.gen as gen


@gen.coroutine
def load_cache(mc):
    cache = {}
    initialize_cache(cache)
    yield load_course_maps(mc, cache)
    yield load_bktf_states(mc, cache)
    # yield load_checkpoints(mc, cache)
    return cache


def initialize_cache(cache):
    cache['course_enrollments'] = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: False)))
    cache['enrollments_insertstamp'] = datetime.datetime(1,1,1,1,1)
    cache['course_maps'] \
    = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {})))
    cache['course_maps_insertstamp'] = datetime.datetime(1,1,1,1,1)
    cache['bktf_states'] \
    = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {})))
    cache['bktf_states_insertstamp'] = datetime.datetime(1,1,1,1,1)
    cache['ownerships'] = defaultdict(lambda: defaultdict(lambda: []))
    cache['platform_uid_fullname'] = defaultdict(lambda: {})
    cache['platform_uid_email'] = defaultdict(lambda: {})


@gen.coroutine
def load_course_maps(mc, cache):
    core_course_maps = mc.core.course_maps
    course_maps_collection = core_course_maps.find().sort('insertstamp')
    while(yield course_maps_collection.fetch_next):
        course_map = course_maps_collection.next_object()
        platform = course_map['platform']
        course_name = course_map['course_name']
        mapping_name = course_map['mapping_name']
        cache['course_maps'][platform][course_name][mapping_name] = course_map
        cache['course_maps_insertstamp'] \
        = max(cache['course_maps_insertstamp'], course_map['insertstamp'])


@gen.coroutine
def load_enrollments(mc, cache):
    core_enrollments = mc.core.enrollments
    enrollments_collection = core_enrollments.find().sort('insertstamp')
    while(yield enrollments_collection.fetch_next):
        enrollment = enrollments_collection.next_object()
        platform = enrollment['platform']
        course_name = enrollment['course_name']
        platform_uid = enrollment['platform_uid']
        cache['course_enrollments'][platform][course_name][platform_uid] = True
        cache['enrollments_insertstamp'] \
        = max(cache['enrollments_insertstamp'], enrollment['insertstamp'])


@gen.coroutine
def load_bktf_states(mc, cache):
    bktf_states = mc.bktf.states
    bktf_states_collection = bktf_states.find().sort('insertstamp')
    while(yield bktf_states_collection.fetch_next):
        bktf_state = bktf_states_collection.next_object()
        platform = bktf_state['platform']
        course_name = bktf_state['course_name']
        mapping_name = bktf_state['mapping_name']
        platform_uid = bktf_state['platform_uid']
        if type(platform_uid) is int:
            continue
        cache['bktf_states'][platform][course_name][mapping_name][platform_uid] \
        = bktf_state
        cache['bktf_states_insertstamp'] \
        = max(cache['bktf_states_insertstamp'], bktf_state['insertstamp'])


@gen.coroutine
def update_enrollments(mc, cache):
    core_enrollments = mc.core.enrollments
    enrollments_collection = core_enrollments.find({
        'insertstamp': {'$gt': cache['enrollments_insertstamp']}
    }).sort('insertstamp')
    while(yield enrollments_collection.fetch_next):
        enrollment = enrollments_collection.next_object()
        platform = enrollment['platform']
        course_name = enrollment['course_name']
        platform_uid = enrollment['platform_uid']
        cache['course_enrollments'][platform][course_name][platform_uid] = True
        cache['enrollments_insertstamp'] \
        = max(cache['enrollments_insertstamp'], enrollment['insertstamp'])


@gen.coroutine
def update_bktf_states(mc, cache):
    bktf_states = mc.bktf.states
    bktf_states_collection = bktf_states.find({
        'insertstamp': {'$gt': cache['bktf_states_insertstamp']},
    }).sort('insertstamp')
    while(yield bktf_states_collection.fetch_next):
        bktf_state = bktf_states_collection.next_object()
        platform = bktf_state['platform']
        course_name = bktf_state['course_name']
        mapping_name = bktf_state['mapping_name']
        platform_uid = bktf_state['platform_uid']
        cache['bktf_states'][platform][course_name][mapping_name][platform_uid] \
        = bktf_state
        cache['bktf_states_insertstamp'] \
        = max(cache['bktf_states_insertstamp'], bktf_state['insertstamp'])

