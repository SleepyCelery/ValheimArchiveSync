import os
import time


# 上传到服务器的文件格式为 世界名_上传人_上传时间戳

def get_timestamp():
    return int(time.time())


def timestamp_convert(timestamp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp)))


def check_filename(filename):
    info = filename.split("_")
    try:
        if info[0] != '' and info[1] != '' and len(info[2]) == 14:
            return True
        else:
            return False
    except IndexError:
        return False


def archives_info():
    name_list = os.listdir('./Archive')
    archive_info = []
    for i in name_list:
        if check_filename(i):
            info = i.split('_')
            archive_info.append(
                {'world_name': info[0], 'upload_user': info[1], 'upload_time': timestamp_convert(info[2].split(".")[0]),
                 'archive_name': i})
    return archive_info


if __name__ == '__main__':
    print(check_filename('Celerysworld_chaoyihu_1617805085.zip'))
