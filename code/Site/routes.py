# Copyright (c) 2017 Jonathan Bassen, Stanford University

from activity_text import ActivityTextHandler
from course import CourseHandler
from home import HomeHandler
from login import LagunitaLoginHandler
from login import SUClassLoginHandler
from login import LogoutHandler
from mapping import MappingHandler
from module import ModuleHandler
from objective import ObjectiveHandler
from landing import LandingHandler
from skill import SkillHandler

def get_routes():
    cg = r"/([0-9a-zA-Z\%\:\+\_\-\.]+)"
    return [
        (r"/", HomeHandler),
        (r"/edx/login", LagunitaLoginHandler),
        (r"/logout", LogoutHandler),
        (r"/lagunita/dump", ActivityTextHandler),
        (cg, LandingHandler),
        (cg + cg, CourseHandler),
        (cg + cg + cg, MappingHandler),
        (cg + cg + cg + cg, ModuleHandler),
        (cg + cg + cg + cg + cg, ObjectiveHandler),
        (cg + cg + cg + cg + cg + cg, SkillHandler),
    ]
