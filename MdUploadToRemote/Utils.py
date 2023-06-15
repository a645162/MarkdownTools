# -*- coding: utf-8 -*-
"""
@File   :   Utils.py
@Date   :   2023/6/8
@Author :   Haomin Kong
@IDE    :   Pycharm
"""

import platform
import re


def is_windows():
    return str(platform.system()).find("Windows") != -1


def is_linux():
    return str(platform.system()).find("Linux") != -1


def is_url(text):
    url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text)
    return len(url) != 0


def backslash_to_slash(path):
    r = path

    while r.find('\\') != -1:
        r = r.replace('\\', '/')
    return r


def slash_to_backslash(path):
    r = path

    if is_windows():
        while r.find('/') != -1:
            r = r.replace('/', '\\')
    return r
