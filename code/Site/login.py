# Copyright (c) 2017 Jonathan Bassen, Stanford University

import os
import tornado.escape as escape
import tornado.gen as gen
import tornado.httputil as httputil
import tornado.web as web
import urllib

from base import BaseHandler
from cache import update_enrollments
from db import upsert_from_roster


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/")



class LagunitaLoginHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        code_argument = self.get_argument('code', '')

        if self.current_user: #3
            self.redirect('/lagunita')

        elif code_argument: #2
            auth_header = yield self.fetch_auth_header(code_argument)
            username = yield self.fetch_username(auth_header)
            course_names = yield self.cache_ownerships(auth_header, username)
            yield self.cache_upsert_roster_data(auth_header, course_names)
            self.set_secure_cookie('user', username)
            self.redirect('/lagunita')

        else: #1
            auth_args = {
                'redirect_uri': os.environ['LAGUNITA_REDIRECT_URL'],
                'client_id': os.environ['LAGUNITA_CLIENT_ID'],
                'client_secret': os.environ['LAGUNITA_CLIENT_SECRET'],
                'response_type': 'code',
                "scope": "openid profile",
            }
            self.redirect(httputil.url_concat(\
                os.environ['LAGUNITA_AUTHORIZE_URL'],
                auth_args,
            ))


    @gen.coroutine
    def fetch_auth_header(self, code_argument):
            body = urllib.parse.urlencode({
                'redirect_uri': os.environ['LAGUNITA_REDIRECT_URL'],
                'code': code_argument,
                'client_id': os.environ['LAGUNITA_CLIENT_ID'],
                'client_secret': os.environ['LAGUNITA_CLIENT_SECRET'],
                'grant_type': 'authorization_code',
            })
            token_response = yield self.httpc.fetch(\
                os.environ['LAGUNITA_TOKEN_URL'],
                method='POST',
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                body=body,
            )
            token_response_args = escape.json_decode(token_response.body)
            token_type = str(token_response_args['token_type'])
            access_token = str(token_response_args['access_token'])
            return token_type + ' ' + access_token


    @gen.coroutine
    def fetch_username(self, auth_header):
        info_response = yield self.httpc.fetch(\
            os.environ['LAGUNITA_USER_INFO_URL'],
            headers={'Authorization': auth_header},
        )
        info_response_args = escape.json_decode(info_response.body)
        return info_response_args['preferred_username']


    @gen.coroutine
    def cache_ownerships(self, auth_header, username):
        platform = 'lagunita'
        ownerships_response = yield self.httpc.fetch(\
            os.environ['LAGUNITA_ENROLLMENT_URL'],
            headers={'Authorization': auth_header},
        )
        ownerships = self.cache['ownerships'][platform]
        ownerships[username] = []
        enrollments = escape.json_decode(ownerships_response.body)
        for enrollment in enrollments:
            course_details = enrollment.get('course_details', {})
            course_name = course_details.get('course_id', '')
            if course_name in self.cache['course_maps'][platform]:
                ownerships[username].append(course_name)
                self.log.error('owns: ' + course_name)
        return ownerships[username]


    @gen.coroutine
    def cache_upsert_roster_data(self, auth_header, course_names):
        platform = 'lagunita'
        yield update_enrollments(self.mc, self.cache)
        for course_name in course_names:
            roster = yield self.fetch_roster(auth_header, course_name)
            yield upsert_from_roster(self.mc, self.cache, roster, platform, course_name)
            self.cache_platform_uid_pii(roster)


    @gen.coroutine
    def fetch_roster(self, auth_header, course_name):
        self.log.error(course_name)
        roster_response = yield self.httpc.fetch(\
            os.environ['LAGUNITA_ROSTER_URL'] + course_name,
            headers={'Authorization': auth_header}
        )
        roster_response_args = escape.json_decode(\
            escape.json_decode(roster_response.body)
        )
        lagunita_roster = roster_response_args.get('roster')
        return [
            {
                'fullname': enrollment.get('name'),
                'lagunita_uid': str(enrollment.get('user_id')),
                'email': enrollment.get('email'),
            }
            for enrollment in lagunita_roster
            if enrollment.get('is_staff') == 0
        ]


    @gen.coroutine
    def cache_platform_uid_pii(self, roster):
        platform = 'lagunita'
        for learner in roster:
            platform_uid = learner['lagunita_uid']
            email = learner['email']
            fullname = learner['fullname']
            self.cache['platform_uid_fullname'][platform][platform_uid] = fullname
            self.cache['platform_uid_email'][platform][platform_uid] = email
