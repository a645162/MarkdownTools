# -*- coding: utf-8 -*-
"""
@File   :   oss_upload.py
@Date   :   2023/6/10
@Author :   Haomin Kong
@IDE    :   Pycharm
"""
import sys

import oss2
import os
import MdUploadToRemote.service.aliyunoss.oss_config
import re
import utils


class OssUpload(object):

    def __init__(self):

        self.oss_config = MdUploadToRemote.service.aliyunoss.oss_config.OssConfig()

        # 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
        self.auth = oss2.Auth(self.oss_config.accessKeyId, self.oss_config.accessKeySecret)
        # # Endpoint以杭州为例，其它Region请按实际情况填写。
        self.bucket = oss2.Bucket(self.auth, self.oss_config.server_url, self.oss_config.bucketName)

    def upload_pic(self, md_info):
        img_list = md_info['img_list']

        upload_results = []

        for img_info in img_list:
            local_path = img_info['img_absolute_path']
            remote_path = self.oss_config.target_base_path + img_info['target_path']
            if remote_path.startswith("/"):
                remote_path = remote_path[1:]
            remote_url = self.oss_config.domain + "/" + remote_path + self.oss_config.parameters

            d = {'local_path': local_path, 'remote_path': remote_path,
                 'remote_url': remote_url, 'upload': False, 'ori_relative_path': img_info['ori_relative_path']}

            # 这句话调试的时候用于添加错误，模拟错误！
            # remote_path = "/" + remote_path

            print((remote_path, local_path))
            try:
                if self.bucket.object_exists(remote_path):
                    print("文件已经存在", local_path)
                else:
                    self.bucket.put_object_from_file(remote_path, local_path)
                print(remote_url)
                d['upload'] = True
                print()
            except Exception as e:
                print("上传出错！", local_path)

            upload_results.append(d)
        print()

        return {'md_path': md_info['md_path'],
                'md_dir_path': md_info['md_dir_path'],
                'md_file_name': md_info['md_file_name'],
                'upload_results': upload_results}
