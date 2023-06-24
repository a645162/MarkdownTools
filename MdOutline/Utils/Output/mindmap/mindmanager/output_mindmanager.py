import hashlib
import uuid
import os
import shutil


def get_mm_guid(length=22):
    hl = hashlib.md5()
    hl.update(str(uuid.uuid1()).encode("utf-8"))
    return str(hl.hexdigest())[:length]


def get_current_directory():
    return os.path.dirname(os.path.abspath(__file__))


py_root_directory = get_current_directory()
template_dir = os.path.join(py_root_directory, 'template')
work_dir = os.path.join(py_root_directory, 'workdir')


def copy_all_files(ori_directory_path, target_directory_path):
    for folder_path, folders, files in os.walk(ori_directory_path):
        target_dir = folder_path.replace(ori_directory_path, target_directory_path)

        if not os.path.exists(target_dir):
            os.mkdir(target_dir)

        for file in files:
            file_path = os.path.join(folder_path, file)
            try:
                shutil.copy(file_path, target_dir)
            except Exception as exc:
                print(exc)


def handle_directory():
    # 清空工作目录
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir)
    os.mkdir(work_dir)

    # 模板拷贝到工作目录，不操作模板
    copy_all_files(template_dir, work_dir)


def output_mindmanager(md_node, md_path):
    handle_directory()
