import os
import re

from MdUtils.file_utils import judge_file_encoding
from MdUtils.utils import is_url, backslash_to_slash, correct_slash

re_md_pic = re.compile(r'!\[.*]\(.+\..+\)')
re_md_pic_relative_path = re.compile(r'\(.+\..+\)')
re_md_pic_title = re.compile(r'!\[.*]\(')
re_md_pic_annotation = re.compile(r'".*"\s*\)')
re_md_pic_include_annotation = re.compile(r'\(.+\..+".*"\s*\)')
re_md_pic_exclude_annotation = re.compile(r'\(.+\..+\)')


def parse_md_file_img(md_path, md_code, max_parent_level):
    md_code = md_code.strip()
    if len(md_code) == 0:
        file_encoding = judge_file_encoding(md_path)
        try:
            f = open(md_path, mode='r', encoding=file_encoding)
            md_code = f.read()
            f.close()
        except Exception as e:
            print(e.args)

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
        res = re.findall(re_md_pic_relative_path, md_pic_code)

        if len(res) == 1:
            img_relative_path = res[0].strip()
        else:
            continue

        res = re.findall(re_md_pic_include_annotation, img_relative_path)
        if len(res) == 1:
            # print("find annotation")
            res = re.findall(re_md_pic_annotation, img_relative_path)
            if len(res) == 1:
                img_relative_path = img_relative_path[1:].replace(res[0], "").strip()
            else:
                continue
        elif len(res) == 0:
            img_relative_path = img_relative_path[1:-1].strip()
        else:
            continue

        # 过滤掉已经是在线链接的图片
        if is_url(img_relative_path):
            continue

        img_absolute_path = os.path.join(md_dir_path, correct_slash(img_relative_path))

        # 根据 level级 父目录 生成路径
        md_dir_relative_path = ""
        actual_level = min(max_parent_level, len(md_parent))
        for i in range(actual_level - 1, -1, -1):
            md_dir_relative_path += md_parent[i] + "/"

        img_list.append(
            {
                'img_absolute_path': img_absolute_path,
                'target_path': "/" + md_dir_relative_path + backslash_to_slash(img_relative_path),
                'ori_relative_path': img_relative_path
            }
        )

    return {
        'md_path': md_path,
        'md_dir_path': md_dir_path,
        'md_file_name': md_file_name,
        'img_list': img_list
    }
