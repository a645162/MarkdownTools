# -*- coding: utf-8 -*-
"""
@File   :   oss_main.py
@Date   :   2023/6/8
@Author :   Haomin Kong
@IDE    :   Pycharm
"""

import oss2
import os
import oss_config
import re
import utils

oss_config = oss_config.OssConfig()

re_md_pic = re.compile(r'!\[.*\]\(.+\..+\)')
re_md_pic_other = re.compile(r'\(.+\..+\)')

# 上传逻辑

# 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
auth = oss2.Auth(oss_config.accessKeyId, oss_config.accessKeySecret)
# # Endpoint以杭州为例，其它Region请按实际情况填写。
bucket = oss2.Bucket(auth, oss_config.server_url, oss_config.bucketName)

# 设置存储空间为私有读写权限。
# bucket.create_bucket(oss2.models.BUCKET_ACL_PUBLIC_READ)

md_path = r'H:\Prj\MarkdownTools\oss\test\testmd.md'


def parse_md_file(md_path, max_parent_level):
    # md 文件信息获取
    # md_path = r'H:\testmd.md'
    md_file_name = os.path.basename(md_path)
    md_dir_path = os.path.dirname(md_path)

    tmp_md_dir_path = md_dir_path
    md_parent = []
    while len(os.path.basename(tmp_md_dir_path)) > 0:
        md_parent.append(os.path.basename(tmp_md_dir_path))
        tmp_md_dir_path = os.path.dirname(tmp_md_dir_path)

    md_code = ""
    try:
        f = open(md_path)
        md_code = f.read()
        f.close()
    except Exception as e:
        print(e.args)

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

    return {'md_dir_path': md_dir_path,
            'md_file_name': md_file_name,
            'img_list': img_list}


def upload_pic(md_info):
    img_list = md_info['img_list']

    final_result = []

    for img_info in img_list:
        local_path = img_info['img_absolute_path']
        remote_path = oss_config.target_base_path + img_info['target_path']
        if remote_path.startswith("/"):
            remote_path = remote_path[1:]
        remote_url = oss_config.domain + "/" + remote_path + oss_config.parameters

        d = {'local_path': local_path, 'remote_path': remote_path,
             'remote_url': remote_url, 'upload': False, 'ori_relative_path': img_info['ori_relative_path']}

        # 这句话调试的时候用于添加错误，模拟错误！
        remote_path = "/" + remote_path

        print((remote_path, local_path))
        try:
            bucket.put_object_from_file(remote_path, local_path)
            print(remote_url)
            d['upload'] = True
            print()
        except Exception as e:
            print("上传出错！", local_path)

        final_result.append(d)
    print()


def modify_md_file(md_path, final_result):
    pass


md_info = parse_md_file(md_path=md_path, max_parent_level=oss_config.max_parent_level)
upload_pic(md_info)

print()
# bucket.put_object_from_file('<yourObjectName>', 'img_path')
