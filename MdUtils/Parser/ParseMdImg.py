import os
import re

from MdUtils.File.FilesUtils import Read_File
from MdUtils.Utils import is_url, backslash_to_slash, correct_slash


class ImgLocationType:
    ALL = 0
    NETWORK = 1
    LOCAL = 2


def parse_md_code_img_list(md_code, mode):
    img_list = []

    re_md_pic = re.compile(r'!\[.*]\(.+\..+\)')
    re_md_pic_relative_path = re.compile(r'\(.+\..+\)')
    # re_md_pic_title = re.compile(r'!\[.*]\(')
    re_md_pic_annotation = re.compile(r'".*"\s*\)')
    re_md_pic_include_annotation = re.compile(r'\(.+\..+".*"\s*\)')
    # re_md_pic_exclude_annotation = re.compile(r'\(.+\..+\)')

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

        this_img = {'img_path': img_relative_path}

        if is_url(img_relative_path):
            this_img['ImgLocationType'] = ImgLocationType.NETWORK
            if mode == ImgLocationType.LOCAL:
                continue
        else:
            this_img['ImgLocationType'] = ImgLocationType.LOCAL
            if mode == ImgLocationType.NETWORK:
                continue

        img_list.append(this_img)

    return img_list


def parse_md_file_img_upload_list(md_path, md_code, max_parent_level=2):
    md_code = md_code.strip()

    if len(md_code) == 0:
        md_code = Read_File(md_path)

    md_file_name = os.path.basename(md_path)
    md_dir_path = os.path.dirname(md_path)

    tmp_md_dir_path = md_dir_path
    md_parent = []
    while len(os.path.basename(tmp_md_dir_path)) > 0:
        md_parent.append(os.path.basename(tmp_md_dir_path))
        tmp_md_dir_path = os.path.dirname(tmp_md_dir_path)

    # md文件解析
    img_list = parse_md_code_img_list(md_code, ImgLocationType.LOCAL)
    md_img_update_list = []

    for img in img_list:

        img_relative_path = img['img_path']

        img_absolute_path = os.path.join(md_dir_path, correct_slash(img_relative_path))

        # 根据 level级 父目录 生成路径
        md_dir_relative_path = ""
        actual_level = min(max_parent_level, len(md_parent))
        for i in range(actual_level - 1, -1, -1):
            md_dir_relative_path += md_parent[i] + "/"

        md_img_update_list.append(
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
        'img_list': md_img_update_list
    }


def parse_md_file_img_download_list(md_code, max_parent_level=2):
    md_code = md_code.strip()
    if len(md_code) == 0:
        return None

    # md文件解析
    img_list = parse_md_code_img_list(md_code, ImgLocationType.NETWORK)
    md_img_download_list = []

    for img in img_list:

        img_relative_path = img['img_path'].strip()
        this_file = {'remote_url': img_relative_path}
        img_relative_path = img_relative_path[img_relative_path.find("://") + 3:]
        img_relative_path = img_relative_path[img_relative_path.find("/") + 1:]

        # 去除参数，因为目录/文件名不会允许带问号的
        index = img_relative_path.find('?')
        if index > 0:
            img_relative_path = img_relative_path[:index]

        # 根据 level级 父目录 生成路径
        img_dir_relative_path = ""
        img_url_parent_list = img_relative_path.split("/")
        img_url_parent_final = img_url_parent_list[-max_parent_level - 1:-1]

        for i in range(len(img_url_parent_final)):
            img_dir_relative_path += img_url_parent_final[i] + "/"

        file_name = img_url_parent_list[-1]

        img_dir_relative_path += file_name

        # print(img_dir_relative_path)

        this_file['img_dir_relative_path'] = img_dir_relative_path

        md_img_download_list.append(this_file)

    return md_img_download_list
