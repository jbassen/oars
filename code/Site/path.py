from collections import defaultdict
import tornado.escape as escape

def url_unescape_path(username, platform, course_name,
mapping_name, module_name, objective_name, skill_name, activity_name):
    path = {}
    path['username'] = escape.xhtml_escape(username)
    path['platform'] = platform
    path['course_name'] = course_name
    path['mapping_name'] = escape.url_unescape(mapping_name)
    path['module_name'] = escape.url_unescape(module_name)
    path['objective_name'] = escape.url_unescape(objective_name)
    path['skill_name'] = escape.url_unescape(skill_name)
    path['activity_name'] = escape.url_unescape(activity_name)
    return path


def check_path(cache, path):
    username = path['username']
    platform = path['platform']
    course_name = path['course_name']
    mapping_name = path['mapping_name']
    module_name = path['module_name']
    objective_name = path['objective_name']
    skill_name = path['skill_name']
    activity_name = path['activity_name']

    platform_maps = cache['course_maps']
    if platform not in platform_maps:
        return 'home'
    course_maps = platform_maps[platform]
    ownerships = cache['ownerships'][platform][username]
    if (course_name not in ownerships):
        return 'platform'
    mappings = course_maps[course_name]
    if mapping_name not in mappings:
        return 'course'
    module_names = mappings[mapping_name]['modules']
    if module_name not in module_names:
        return 'mapping'
    objective_names = mappings[mapping_name]['m_to_o'].get(module_name, {})
    if objective_name not in objective_names:
        return 'module'
    skill_names = mappings[mapping_name]['o_to_s'].get(objective_name, {})
    if skill_name not in skill_names:
        return 'objective'
    activity_names = mappings[mapping_name]['s_to_a'].get(skill_name, {})
    if activity_name not in activity_names:
        return 'skill'
    else:
        return 'activity'