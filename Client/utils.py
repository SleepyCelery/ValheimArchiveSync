import os
import time
import zipfile

folder_path = os.getenv('APPDATA').rstrip("Roaming") + '/LocalLow/IronGate/Valheim/worlds/'
file_extension = ['db', 'fwl']


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


def check_valheim_folder():
    return os.path.exists(folder_path)


def create_valheim_folder():
    os.makedirs(folder_path)


def list_archives():
    if check_valheim_folder():
        file_list = os.listdir(folder_path)
        all_archives = []
        for index, value in enumerate(file_list):
            if value.split(".")[-1] in file_extension:
                all_archives.append(value.split('.')[0])
        all_archives = list(set(all_archives))
        return all_archives


def zip_archive(archive_name, upload_user):
    if check_valheim_folder():
        zipname = archive_name + '_' + upload_user + '_' + str(get_timestamp()) + '.zip'
        z = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)
        z.write(folder_path + archive_name + '.db', archive_name + '.db')
        z.write(folder_path + archive_name + '.fwl', archive_name + '.fwl')
        z.close()


def unzip_archive(archive_path):
    if check_valheim_folder():
        r = zipfile.is_zipfile(archive_path)
        if r:
            fz = zipfile.ZipFile(archive_path)
            for file in fz.namelist():
                fz.extract(file, folder_path)
                print('成功提取文件{}至目标文件夹！'.format(file))


def clear(): os.system('cls')


def pause(): os.system('pause')

if __name__ == '__main__':
    unzip_archive('Celerysworld_chaoyihu_1617868906.zip')