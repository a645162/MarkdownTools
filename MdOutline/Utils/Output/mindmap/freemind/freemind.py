import time


def get_freemind_time_now_str():
    get_freemind_time_str(time.time())


def get_freemind_time_str(target_time):
    return str(target_time).replace('.', '')[:13]

