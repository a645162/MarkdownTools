# -*- coding: utf-8 -*-
"""
@File   :   outline_config.py
@Date   :   2023/6/15
@Author :   Haomin Kong
@IDE    :   Pycharm
"""

import configparser
import os

from MdUtils.File.PathUtils import trim_relative_path


class OutlineConfig:

    def __init__(self, path='outline_config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), path), encoding='utf-8')

        # program
        self.conflict = self.config.get('program', 'conflict').strip()
        if self.conflict == 'replace':
            self.conflict = 1
        elif self.conflict == 'backup':
            self.conflict = 2
        else:
            self.conflict = 0

        # todolist
        self.todolist_target_base_path = trim_relative_path(self.config.get('todolist', 'target_base_path'))
        self.md_todolist_enable = self.config.get('todolist', 'md_todolist_enable').strip() == '1'

        # mindmap
        self.mindmap_target_base_path = trim_relative_path(self.config.get('mindmap', 'target_base_path'))
        self.xmind_enable = self.config.get('mindmap', 'xmind_enable').strip() == '1'
