# Copyright (c) 2017 Jonathan Bassen, Stanford University

import copy
import motor.motor_tornado as motor_tornado
import os
from pymongo import ReturnDocument
import ssl
import tornado.gen as gen


def setup_db():
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
def upsert_core_log(event, application):
    try:
        core_logs = application.mc.core.logs
        result = yield core_logs.update_one(
            filter=event,
            update={
                '$set': event,
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
