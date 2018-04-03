# Copyright (c) 2017 Jonathan Bassen, Stanford University

import datetime
import tornado.escape as escape
import tornado.gen as gen
import tornado.web as web
import logging
import numbers
import os
import re
import json


from db import upsert_core_log


def extract_grade(payload):
    try:
        raw_max_grade = float(payload.get('max_grade'))
        raw_grade = float(payload.get('grade'))
        if raw_max_grade > 0.0:
            grade = raw_grade / raw_max_grade
            max_grade = 1.0
        else:
            grade = 0.0
            max_grade = 0.0
        return (grade, max_grade)
    except:
        return (None, None)


def extract_authorized_payload(request_headers, request_body, application, platform):
    if platform == 'lagunita':
        event_key = os.environ['LAGUNITA_EVENT_KEY']
    else:
        return None
    escaped_key = escape.url_escape(event_key)
    authorized_string = 'oauth_consumer_key="' + escaped_key + '"'
    auth_string = request_headers.get('Authorization', '')
    auth_list = auth_string.split()
    event_is_authorized = False
    for auth_arg in auth_list:
        if auth_arg == authorized_string:
            event_is_authorized = True
        elif auth_arg == (authorized_string + ','):
            event_is_authorized = True
    if not event_is_authorized:
        application.log.error('auth error on header: ' + auth_string)
        return None
    event_json = escape.json_decode(request_body.decode('utf-8'))
    if not event_json:
        return None
    payload = event_json.get('payload')
    return payload


def extract_event(request_headers, request_body, application, platform):

    try:
        payload = extract_authorized_payload(\
            request_headers, request_body, application, platform,
        )
        if not payload:
            return None
        timestamp = datetime.datetime.strptime(\
            payload.get('timestamp'),
            '%Y-%m-%dT%H:%M:%S.%f',
        )
        platform_uid = str(payload.get('user_id'))
        course_name = str(payload.get('course_id'))
        activity_name = payload.get('resource_id', '')\
            .split('/')[-1].split('@')[-1]
        grade, max_grade = extract_grade(payload)
        if (not platform or not timestamp or not platform_uid or\
        not course_name or not activity_name or grade==None or max_grade==None):
            return None
        problem_question_name = payload.get('problem_question_name', '')
        if problem_question_name:
            activity_name += (':' + problem_question_name)
        event = {
            'platform': platform,
            'course_name': course_name,
            'activity_name': activity_name,
            'platform_uid': platform_uid,
            'timestamp': timestamp,
            'max_grade': max_grade,
            'grade': grade,
        }
        return event

    except(ValueError):
        return None


@gen.coroutine
def handle_event(request_headers, request_body, application, platform):
    event = extract_event(request_headers, request_body, application, platform)
    if not event:
        application.log.error('parse error on: ' + request_body.decode('utf-8'))
        return None
    core_log_result = yield upsert_core_log(event, application)
    if not core_log_result:
        application.log.error('logs error on: ' + request_body.decode('utf-8'))
        return None
    return 'OK'


class LagunitaEventHandler(web.RequestHandler):

    @gen.coroutine
    def put(self):
        platform = 'lagunita'
        result = yield handle_event(\
            self.request.headers, self.request.body, self.application, platform,
        )
        if result:
            self.write(result)
        else:
            raise web.HTTPError(400)
