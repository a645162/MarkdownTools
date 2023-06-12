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

import utils
from MdUtils.file_utils import judge_file_encoding
from config import upload_config
from service.aliyunoss.oss_upload import OssUpload
from service.qiniuyun.qiniu_upload import QiniuUpload

upload_config = upload_config.UploadConfig()

re_md_pic = re.compile(r'!\[.*\]\(.+\..+\)')
re_md_pic_other = re.compile(r'\(.+\..+\)')

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


def parse_md_file(md_path, md_code, max_parent_level):
    # md 文件信息获取
    # md_path = r'H:\testmd.md'
    md_file_name = os.path.basename(md_path)
    md_dir_path = os.path.dirname(md_path)

    tmp_md_dir_path = md_dir_path
    md_parent = []
    while len(os.path.basename(tmp_md_dir_path)) > 0:
        md_parent.append(os.path.basename(tmp_md_dir_path))
        tmp_md_dir_path = os.path.dirname(tmp_md_dir_path)

    # md文件解析
    img_list = []

    re_result = re.findall(re_md_pic, md_code)
    for md_pic_code in re_result:
        res = re.findall(re_md_pic_other, md_pic_code)
        img_relative_path = ""
        if len(res) == 1:
            img_relative_path = res[0].strip()[1:-1].strip()

        # 过滤掉已经是在线链接的图片
        if utils.is_url(img_relative_path):
            continue

        # img_relative_path = 'img/1686209662200.png'
        img_absolute_path = os.path.join(md_dir_path, utils.slash_to_backslash(img_relative_path))

        # 根据 level级 父目录 生成路径
        md_dir_relative_path = ""
        actual_level = min(max_parent_level, len(md_parent))
        for i in range(actual_level - 1, -1, -1):
            md_dir_relative_path += md_parent[i] + "/"

        # target_path = oss_config.target_base_path + "/" + md_dir_relative_path + img_relative_path
        # target_url = oss_config.domain + target_path + oss_config.parameters

        img_list.append(
            {
                'img_absolute_path': img_absolute_path,
                'target_path': "/" + md_dir_relative_path + utils.backslash_to_slash(img_relative_path),
                'ori_relative_path': img_relative_path
            }
        )

    return {'md_path': md_path,
            'md_dir_path': md_dir_path,
            'md_file_name': md_file_name,
            'img_list': img_list}


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

    # from chardet.universaldetector import UniversalDetector
    # detector = UniversalDetector()
    # detector.reset()
    # for each in open(md_path, 'rb'):
    #     detector.feed(each)
    #     if detector.done:
    #         break
    # detector.close()
    # file_encoding = detector.result['encoding']
    # confidence = detector.result['confidence']
    #
    # if confidence < 0.75:
    #     file_encoding = 'utf-8'

    file_encoding = judge_file_encoding(md_path)

    md_code = ""
    try:
        f = open(md_path, mode='r', encoding=file_encoding)
        md_code = f.read()
        f.close()
    except Exception as e:
        print(e.args)

    md_info = parse_md_file(md_path=md_path, max_parent_level=upload_config.max_parent_level, md_code=md_code)
    upload_info = upload_pic(md_info=md_info)
    modify_md_file(upload_info=upload_info, md_code=md_code)


if __name__ == '__main__':

    files_list = sys.argv[1:]
    # files_list.append(r'H:\Prj\MarkdownTools\MdUploadToRemote\test\testmd.md')
    # files_list.append(r'/media/konghaomin/PAM963/Data/Obsdian/PC/Windows/Windows Defender.md')

    if len(files_list) == 0:
        print("请将路径作为参数传入！")

    for md_path in files_list:
        print(md_path)
        if os.path.exists(md_path):
            doall(md_path)
