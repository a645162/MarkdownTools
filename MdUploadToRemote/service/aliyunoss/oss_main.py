# -*- coding: utf-8 -*-
"""
@File   :   oss_main.py
@Date   :   2023/6/8
@Author :   Haomin Kong
@IDE    :   Pycharm
"""
import sys

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


# md_path = r'H:\Prj\MarkdownTools\aliyunoss\test\testmd.md'

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


def upload_pic(md_info):
    img_list = md_info['img_list']

    upload_results = []

    for img_info in img_list:
        local_path = img_info['img_absolute_path']
        remote_path = oss_config.target_base_path + img_info['target_path']
        if remote_path.startswith("/"):
            remote_path = remote_path[1:]
        remote_url = oss_config.domain + "/" + remote_path + oss_config.parameters

        d = {'local_path': local_path, 'remote_path': remote_path,
             'remote_url': remote_url, 'upload': False, 'ori_relative_path': img_info['ori_relative_path']}

        # 这句话调试的时候用于添加错误，模拟错误！
        # remote_path = "/" + remote_path

        print((remote_path, local_path))
        try:
            if bucket.object_exists(remote_path):
                print("文件已经存在", local_path)
            else:
                bucket.put_object_from_file(remote_path, local_path)
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

    from chardet.universaldetector import UniversalDetector
    detector = UniversalDetector()
    detector.reset()
    for each in open(md_path, 'rb'):
        detector.feed(each)
        if detector.done:
            break
    detector.close()
    file_encoding = detector.result['encoding']
    confidence = detector.result['confidence']

    if confidence < 0.75:
        file_encoding = 'utf-8'

    md_code = ""
    try:
        f = open(md_path, mode='r', encoding=file_encoding)
        md_code = f.read()
        f.close()
    except Exception as e:
        print(e.args)

    md_info = parse_md_file(md_path=md_path, max_parent_level=oss_config.max_parent_level, md_code=md_code)
    upload_info = upload_pic(md_info=md_info)
    modify_md_file(upload_info=upload_info, md_code=md_code)


if __name__ == '__main__':

    files_list = sys.argv[1:]
    files_list.append(r'H:\Prj\MarkdownTools\MdUploadToRemote\test\testmd.md')

    if len(files_list) == 0:
        print("请将路径作为参数传入！")

    for md_path in files_list:
        print(md_path)
        if os.path.exists(md_path):
            doall(md_path)

# print()
# bucket.put_object_from_file('<yourObjectName>', 'img_path')
