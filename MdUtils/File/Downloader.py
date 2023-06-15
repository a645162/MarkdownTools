import requests


def download2local_simple(url, save_path):
    r = requests.get(url)
    with open(save_path, "wb") as code:
        code.write(r.content)
