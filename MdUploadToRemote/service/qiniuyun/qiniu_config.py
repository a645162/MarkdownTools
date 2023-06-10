# -*- coding: utf-8 -*-
"""
@File   :   qiniu_config.py
@Date   :   2023/6/10
@Author :   Haomin Kong
@IDE    :   Pycharm
"""

import configparser
import os


class QiniuConfig:

    def __init__(self, path='qiniu_config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(path, encoding='utf-8')

        self.access_key = self.config.get('qiniu', 'access_key')
        self.secret_key = self.config.get('qiniu', 'secret_key')

        self.bucket_name = self.config.get('bucket', 'bucket_name')
        self.parameters = self.config.get('bucket', 'parameters')
        # self.region = self.config.get('bucket', 'region')
        self.domain = self.config.get('domain', 'domain')

        # self.server_url = r'http://{}.aliyuncs.com'.format(self.region)
        if len(self.domain) == 0:
            self.domain = r'https://{}.{}.aliyuncs.com'.format(self.bucketName, self.region)

        self.target_base_path = self.config.get('program', 'target_base_path')
        if self.target_base_path.startswith('/'):
            self.target_base_path = self.target_base_path[1:]

        if self.target_base_path.endswith('/'):
            self.target_base_path = self.target_base_path[:-1]
