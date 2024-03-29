import os
import sys

from MdDownloadToLocal.config.download_config import DownloadConfig
from MdUtils.File.Downloader.Downloader import download2local_simple
from MdUtils.File.FilesUtils import read_file
from MdUtils.Parser.ParseMdImg import parse_md_file_img_download_list
from MdUtils.Utils import correct_slash, backslash_to_slash

download_config = DownloadConfig()


def generate_download_list(md_img_download_list, md_path):
    md_dir = os.path.dirname(md_path)

    for i in range(len(md_img_download_list)):
        img_dir_relative_path = md_img_download_list[i]['img_dir_relative_path']
        img_dir_relative_path = download_config.target_base_path + "/" + img_dir_relative_path
        md_img_download_list[i]['img_dir_relative_path'] = backslash_to_slash(img_dir_relative_path)

        abs_path = os.path.join(md_dir, correct_slash(img_dir_relative_path))
        md_img_download_list[i]['abs_path'] = abs_path

    return md_img_download_list


def download_generate_md(md_path, md_code, md_img_download_list):
    if len(md_code.strip()) == 0:
        md_code = read_file(md_path)

    new_md_path = md_path + ".local.md"

    for download_item in md_img_download_list:
        remote_url = download_item['remote_url']
        abs_path = download_item['abs_path']

        download2local_simple(remote_url, abs_path)

        img_dir_relative_path = download_item['img_dir_relative_path']

        md_code = md_code.replace(remote_url, img_dir_relative_path)

    with open(new_md_path, 'w', encoding='utf-8') as file:
        file.write(md_code)


def doall(md_path):
    print("\n\n\n开始", md_path)

    md_code = read_file(md_path)

    md_img_download_list = \
        parse_md_file_img_download_list(max_parent_level=download_config.max_parent_level, md_code=md_code)

    md_img_download_list = generate_download_list(md_img_download_list=md_img_download_list, md_path=md_path)

    download_generate_md(md_path=md_path, md_code=md_code, md_img_download_list=md_img_download_list)


if __name__ == '__main__':

    files_list = sys.argv[1:]

    if len(files_list) == 0:
        print("请将路径作为参数传入！")

    for md_path in files_list:
        print(md_path)
        if os.path.exists(md_path):
            doall(md_path)
