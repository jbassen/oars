import motor.motor_tornado as motor_tornado
import logging
import os
import ssl
import tornado.gen as gen


def get_mongo_client():
    m1 = os.environ['MONGO1_ADDR']
    m2 = os.environ['MONGO2_ADDR']
    m3 = os.environ['MONGO3_ADDR']
    mongo_port = os.environ['MONGO_PORT']
    mongo_usr = os.environ['MONGO_USR']
    mongo_pwd = os.environ['MONGO_PWD']
    mongo_rs = os.environ['MONGO_RS']

    mongo_uri = 'mongodb://'
    mongo_uri += mongo_usr + ':'
    mongo_uri += mongo_pwd + '@'
    mongo_uri += m1 + ':' + mongo_port + ','
    mongo_uri += m2 + ':' + mongo_port + ','
    mongo_uri += m3 + ':' + mongo_port
    mongo_uri += '/?replicaSet=' + mongo_rs

    return motor_tornado.MotorClient(\
        mongo_uri,
        ssl=True,
        ssl_cert_reqs=ssl.CERT_NONE
    )


@gen.coroutine
def upsert_states(mc, cache):
    for platform, platform_state in cache['state'].items():
        for course_name, course_state in platform_state.items():
            for mapping_name, mapping_state in course_state.items():
                for platform_uid, state in mapping_state.items():
                    yield upsert_state(mc, state)


@gen.coroutine
def upsert_state(mc, state):
    try:
        bktf_states = mc.bktf.states
        result = yield bktf_states.update_one(
            filter = {
                'platform': state['platform'],
                'course_name': state['course_name'],
                'mapping_name': state['mapping_name'],
                'platform_uid': state['platform_uid'],
            },
            update = {
                '$set': state,
                '$currentDate': {
                    'insertstamp': True,
                },
            },
            upsert = True,
        )
        return result
    except BaseException as e:
        logging.error( 'mongodb exception: ' + str(e) )
        return None


def get_logs_updates(mc, logs_insertstamp):
    core_logs = mc.core.logs
    logs_collection = core_logs.find({
        'insertstamp': {'$gt': logs_insertstamp}
    }).sort('insertstamp')
    return logs_collection


def get_enrollments_updates(mc, enrollments_insertstamp):
    core_enrollments = mc.core.enrollments
    enrollments_collection = core_enrollments.find({
        'insertstamp': {'$gt': enrollments_insertstamp}
    }).sort('insertstamp')
    return enrollments_collection
