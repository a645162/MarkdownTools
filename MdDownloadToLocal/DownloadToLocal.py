import os
import sys

from MdUtils.File.FilesUtils import Read_File


def doall(md_path):
    print("开始", md_path)

    md_code = Read_File(md_path)

    # md_info = parse_md_file_img_download_list(md_path=md_path, max_parent_level=upload_config.max_parent_level,
    #                                           md_code=md_code)

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
