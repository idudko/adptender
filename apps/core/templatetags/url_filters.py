import re
from django import template

register = template.Library()

def match_url(pattern, path):
    if pattern:
        if re.compile(pattern).match(path):
            return True
    return False

register.filter('match_url', match_url)