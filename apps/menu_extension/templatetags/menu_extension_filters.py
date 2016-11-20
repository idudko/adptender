# -*- coding: utf-8 -*-
import re
from django import template

register = template.Library()

def match_path(patterns, path):
    if patterns:
        for pattern in patterns.splitlines():
            if re.compile(pattern).match(path):
                return True
    return False

register.filter('match_path', match_path)