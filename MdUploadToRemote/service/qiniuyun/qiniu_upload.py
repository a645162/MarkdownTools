# -*- coding: utf-8 -*-
"""
@File   :   qiniu_upload.py
@Date   :   2023/6/10
@Author :   Haomin Kong
@IDE    :   Pycharm
"""
import sys

from qiniu import Auth
from qiniu import BucketManager
from qiniu import put_file

import MdUploadToRemote.service.qiniuyun.qiniu_config


# import utils


class QiniuUpload(object):

    def __init__(self):

        self.qiniu_config = MdUploadToRemote.service.qiniuyun.qiniu_config.QiniuConfig()
        self.q = Auth(self.qiniu_config.access_key, self.qiniu_config.secret_key)
        self.token = self.q.upload_token(self.qiniu_config.bucket_name)
        self.bucket = BucketManager(self.q)

    def upload_pic(self, md_info):
        img_list = md_info['img_list']

        upload_results = []

        for img_info in img_list:
            local_path = img_info['img_absolute_path']
            remote_path = self.qiniu_config.target_base_path + img_info['target_path']
            if remote_path.startswith("/"):
                remote_path = remote_path[1:]
            remote_url = self.qiniu_config.domain + "/" + remote_path + self.qiniu_config.parameters

            d = {'local_path': local_path, 'remote_path': remote_path,
                 'remote_url': remote_url, 'upload': False, 'ori_relative_path': img_info['ori_relative_path']}

            # 这句话调试的时候用于添加错误，模拟错误！
            # remote_path = "/" + remote_path

            print((remote_path, local_path))
            try:
                ret, info = self.bucket.stat(self.qiniu_config.bucket_name, remote_path)
                if str(info.status_code) == '200':
                    print("文件已经存在", local_path)
                else:
                    ret, info = put_file(self.token, remote_path, local_path, check_crc=True)
                    # print(info.ok())
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
