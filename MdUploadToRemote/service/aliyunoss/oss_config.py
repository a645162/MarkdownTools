# -*- coding: utf-8 -*-
"""
@File   :   oss_config.py
@Date   :   2023/6/8
@Author :   Haomin Kong
@IDE    :   Pycharm
"""

import configparser
import os


class OssConfig:

    def __init__(self, path='oss_config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), path), encoding='utf-8')

        self.accessKeyId = self.config.get('aliyun', 'accessKeyId')
        self.accessKeySecret = self.config.get('aliyun', 'accessKeySecret')

        self.bucketName = self.config.get('bucket', 'bucketName')
        self.parameters = self.config.get('bucket', 'parameters')

        self.region = self.config.get('bucket', 'region')
        self.domain = self.config.get('bucket', 'domain')
        self.server_url = r'http://{}.aliyuncs.com'.format(self.region)
        if len(self.domain) == 0:
            self.domain = r'https://{}.{}.aliyuncs.com'.format(self.bucketName, self.region)

        self.target_base_path = self.config.get('program', 'target_base_path')
        if self.target_base_path.startswith('/'):
            self.target_base_path = self.target_base_path[1:]
        if self.target_base_path.endswith('/'):
            self.target_base_path = self.target_base_path[:-1]

        self.max_parent_level = self.config.get('program', 'max_parent_level')
        if len(self.max_parent_level) == 0:
            self.max_parent_level = '2'
        self.max_parent_level = int(self.max_parent_level)
