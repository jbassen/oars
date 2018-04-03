# Copyright (c) 2017 Jonathan Bassen, Stanford University

import os
import tornado.escape as escape
import tornado.gen as gen
import tornado.httputil as httputil
import tornado.web as web
import urllib

from db import upsert_activity_data

def extract_authorized_payload(headers, body, application):
    payload = escape.json_decode(request_body.decode('utf-8'))
    if not payload:
        return None
    platform = payload.get('platform')
    event_key = None
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
    return payload


def extract_activity_data(payload):
    platform = payload.get('platform')
    platform_data = []
    courses = payload.get('courses')
    for course_name, activities in course_names.items():
        course_data = {}
        course_data['platform'] = platform
        course_data['course_name'] = course_name
        course_data['problem_to_t'] = {}
        for problem_name, problem_text in activities.items():
            course_data['problem_to_t'][problem_name] = problem_text
        platform_data.append(course_data)
    return platform_data


@gen.coroutine
def handle_activity_text(headers, body, application):
    payload = extract_authorized_payload(headers, body, application)
    if not payload:
        return None
    activity_data = extract_activity_data(payload)
    if not activity_data:
        application.log.error(
            'parse error on: '
            + body.decode('utf-8')
        )
        return None
    upsert_result = yield upsert_activity_data(application.mc, activity_data)
    if not upsert_result:
        application.log.error(
            'activity data error on: '
            + request_body.decode('utf-8')
        )
        return None
    return 'OK'


class ActivityTextHandler(web.RequestHandler):
    @gen.coroutine
    def put(self):
        result = yield handle_activity_text(\
            self.request.headers, self.request.body, self.application
        )
        if result:
            self.write(result)
        else:
            raise web.HTTPError(400)
