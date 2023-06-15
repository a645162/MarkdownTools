# -*- coding: utf-8 -*-
"""
@File   :   download_config.py
@Date   :   2023/6/15
@Author :   Haomin Kong
@IDE    :   Pycharm
"""

import configparser
import os


class DownloadConfig:

    def __init__(self, path='download_config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), path), encoding='utf-8')

        self.type = str(self.config.get('downloader', 'type'))

        self.target_base_path = self.config.get('program', 'target_base_path')
        if self.target_base_path.startswith('/'):
            self.target_base_path = self.target_base_path[1:]
        if self.target_base_path.endswith('/'):
            self.target_base_path = self.target_base_path[:-1]

        self.max_parent_level = self.config.get('program', 'max_parent_level')
        if len(self.max_parent_level) == 0:
            self.max_parent_level = '0'
        self.max_parent_level = int(self.max_parent_level)
