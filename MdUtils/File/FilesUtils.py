import os
import time


def read_file(file_path):
    file_encoding = judge_file_encoding(file_path)

    md_code = ""
    try:
        f = open(file_path, mode='r', encoding=file_encoding)
        md_code = f.read()
        f.close()
    except Exception as e:
        print('读取文件出错！', file_path)
        print(e.args)

    return md_code


def save_file(file_path, text=""):
    file_dir = os.path.dirname(file_path)
    print('即将写出', file_path)
    if os.path.isfile(file_path):
        # ctime = time.localtime(os.path.getctime(todoFilePath))
        mtime = time.localtime(os.path.getmtime(file_path))
        mtime = time.strftime("%Y-%m-%d-%H-%M-%S", mtime)
        print("发现旧的文件，修改日期：")
        print(mtime)
        new_name = "(" + mtime + ")" + file_path

        os.rename(file_path, os.path.join(file_dir, new_name))

    try:
        f = open(file_path, "w", encoding='utf-8')
        f.write(text)
        f.close()
    except:
        print('文件写出失败！')


def judge_file_encoding(file_path):
    from chardet.universaldetector import UniversalDetector
    detector = UniversalDetector()
    detector.reset()
    for each in open(file_path, 'rb'):
        detector.feed(each)
        if detector.done:
            break
    detector.close()
    file_encoding = detector.result['encoding']
    confidence = detector.result['confidence']

    if confidence < 0.75:
        # 置信度过低就认为编码是 UTF-8
        file_encoding = 'utf-8'

    return file_encoding


def mkdir_if_not_exist(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
