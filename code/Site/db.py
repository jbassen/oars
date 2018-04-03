# Copyright (c) 2017 Jonathan Bassen, Stanford University

import motor.motor_tornado as motor_tornado
import logging
import os
from pymongo import ReturnDocument
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
def upsert_from_roster(mc, cache, roster, platform, course_name):
    for record in roster:
        if platform == 'lagunita':
            platform_uid = record['lagunita_uid']
        else:
            continue
        course_enrollments = cache['course_enrollments'][platform][course_name]
        if platform_uid not in course_enrollments:
            yield upsert_enrollment(mc,
                {
                    'platform': platform,
                    'course_name': course_name,
                    'platform_uid': platform_uid,
                },
            )
            course_enrollments[platform_uid] = platform_uid


@gen.coroutine
def upsert_enrollment(mc, enrollment):
    core_enrollments = mc.core.enrollments
    result = yield core_enrollments.find_one_and_update(
        filter=enrollment,
        update={
            '$setOnInsert': enrollment,
            '$currentDate': {
                'insertstamp': True,
            },
        },
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return result

@gen.coroutine
def upsert_activity_data(mc, platform_data):
    try:
        activity_text = mc.core.activity_text
        for course_data in platform_data:
            result = yield activity_text.update_one(
                filter={
                    platform: course_data['platform'],
                    course_name: course_data['course_name'],
                },
                update={
                    '$set': course_data,
                    '$currentDate': {
                        'insertstamp': True,
                    },
                },
                upsert=True,
            )
            return result
    except BaseException as e:
        application.log.error( 'mongodb exception: ' + str(e) )
        return None
