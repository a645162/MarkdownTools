import time


def convert_timestamp_to_time(timestamp):
    time_str = str(timestamp).strip()
    # print(time_str)

    if len(time_str) < 10:
        return None

    if time_str.find('.') != -1:
        if time_str.endswith('.'):
            time_str += '.'
        now = time_str
    else:
        if len(time_str) > 10:
            now = time_str[:10] + '.' + time_str[10:]
        else:
            now = time_str + ".0"

    # print(time.strftime("%Y-%m-%d %H:%M:%S", timeArray))

    return time.localtime(float(now))
