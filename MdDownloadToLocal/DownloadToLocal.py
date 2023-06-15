import os
import sys

from MdDownloadToLocal.config.download_config import DownloadConfig
from MdUtils.File.FilesUtils import Read_File
from MdUtils.Parser.ParseMdImg import parse_md_file_img_download_list
from MdUtils.Utils import correct_slash, backslash_to_slash

download_config = DownloadConfig()


def generate_download_list(md_img_download_list, md_path):
    md_dir = os.path.dirname(md_path)

    for i in range(len(md_img_download_list)):
        img_dir_relative_path = md_img_download_list[i]['img_dir_relative_path']
        img_dir_relative_path = download_config.target_base_path + "/" + img_dir_relative_path
        md_img_download_list[i]['img_relative_path_final'] = backslash_to_slash(img_dir_relative_path)
        img_dir_relative_path = correct_slash(img_dir_relative_path)
        abs_path = os.path.join(md_dir, img_dir_relative_path)
        md_img_download_list[i]['abs_path'] = abs_path

    return md_img_download_list


def doall(md_path):
    print("\n\n\n开始", md_path)

    md_code = Read_File(md_path)

    md_img_download_list = \
        parse_md_file_img_download_list(max_parent_level=download_config.max_parent_level, md_code=md_code)

    md_img_download_list = generate_download_list(md_img_download_list=md_img_download_list, md_path=md_path)

    print()

    # upload_info = upload_pic(md_info=md_info)
    # modify_md_file(upload_info=upload_info, md_code=md_code)


if __name__ == '__main__':

    files_list = sys.argv[1:]

    if len(files_list) == 0:
        print("请将路径作为参数传入！")

    for md_path in files_list:
        print(md_path)
        if os.path.exists(md_path):
            doall(md_path)
