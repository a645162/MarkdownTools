# -*- coding: utf-8 -*-
"""
@File   :   UploadToRemote.py
@Date   :   2023/6/10
@Author :   Haomin Kong
@IDE    :   Pycharm
"""

import os
import re
import sys

from MdUtils.file_utils import judge_file_encoding
from MdUtils.parser.parse_md_img import parse_md_file_img
from config import upload_config
from service.aliyunoss.oss_upload import OssUpload
from service.qiniuyun.qiniu_upload import QiniuUpload

upload_config = upload_config.UploadConfig()

if upload_config.type == '1':
    updateObj = OssUpload()
    upload_pic = updateObj.upload_pic
elif upload_config.type == '2':
    updateObj = QiniuUpload()
    upload_pic = updateObj.upload_pic
elif upload_config.type == '3':
    print('暂时不支持的类型！')
    exit(-1)
elif upload_config.type == '4':
    print('暂时不支持的类型！')
    exit(-1)
elif upload_config.type == '5':
    print('暂时不支持的类型！')
    exit(-1)
else:
    print('暂时不支持的类型！')
    exit(-1)


def modify_md_file(upload_info, md_code):
    md_path = upload_info['md_path']

    if len(md_code) == 0:
        return

    new_md_path = md_path + ".upload.md"

    upload_results = upload_info['upload_results']
    for upload_result in upload_results:
        ori_relative_path = upload_result['ori_relative_path']
        if upload_result['upload']:
            md_code = md_code.replace(ori_relative_path, upload_result['remote_url'])
        else:
            print("出现致命错误！")
            print(upload_result)
            print(upload_results)
            print(upload_info)

    try:
        f = open(new_md_path, encoding='utf-8', mode='w')
        f.write(md_code)
        f.close()
        print(new_md_path)
        print("写出成功！")
    except Exception as e:
        print(e.args)


def doall(md_path):
    print("开始", md_path)

    file_encoding = judge_file_encoding(md_path)

    md_code = ""
    try:
        f = open(md_path, mode='r', encoding=file_encoding)
        md_code = f.read()
        f.close()
    except Exception as e:
        print(e.args)

    md_info = parse_md_file_img(md_path=md_path, max_parent_level=upload_config.max_parent_level, md_code=md_code)
    upload_info = upload_pic(md_info=md_info)
    modify_md_file(upload_info=upload_info, md_code=md_code)


if __name__ == '__main__':

    files_list = sys.argv[1:]
    # files_list.append(r'H:\Prj\MarkdownTools\MdUploadToRemote\test\testmd.md')
    files_list.append(r'/media/konghaomin/PAM963/Data/Obsdian/Linux/Linux/Wayland.md')
    # files_list.append(r'/media/konghaomin/PAM963/Data/Obsdian/Linux/Linux/KDE 双显示器不同 DPI.md')
    # files_list.append(r'H:\Data\Obsdian\Linux\Linux\KDE 双显示器不同 DPI.md')

    if len(files_list) == 0:
        print("请将路径作为参数传入！")

    for md_path in files_list:
        print(md_path)
        if os.path.exists(md_path):
            doall(md_path)
