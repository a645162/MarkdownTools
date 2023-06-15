import os

import requests

from MdUtils.File.FilesUtils import mkdir_if_not_exist


def download2local_simple(url, save_path):
    if os.path.exists(save_path):
        os.remove(save_path)

    mkdir_if_not_exist(os.path.dirname(save_path))

    r = requests.get(url)
    with open(save_path, "wb") as code:
        code.write(r.content)
