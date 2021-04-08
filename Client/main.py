from utils import *
import os
import requests

debug = False
if debug:
    main_url = 'http://127.0.0.1:41356'
else:
    main_url = 'http://www.chaoyihu.top:41356'

if __name__ == '__main__':
    print('----------英灵神殿世界存档同步工具----------')
    print()
    print('Developed by SleepyCelery, Using FastAPI backend')
    print()
    first_flag = True
    if not check_valheim_folder():
        cmd = input('未检测到英灵神殿世界存档文件夹！是否创建？(Y/N)')
        if cmd.lower() == 'y':
            create_valheim_folder()
        else:
            exit()
    while True:
        if first_flag:
            first_flag = False
        else:
            clear()
        print('1. 上传本地存档至服务器')
        print('2. 将服务器存档同步至本地')
        cmd = input('请选择一个项目:')
        if int(cmd) == 1:
            clear()
            print('当前本地存档目录有以下世界文件：')
            archives = list_archives()
            for index, value in enumerate(archives):
                print('{}.{}'.format(index + 1, value))
            choice = int(input('请输入要上传的世界文件序号：')) - 1
            username = input('请输入您的用户名(这将作为您上传存档的身份凭据，请确保其他人能辨别)：')
            if int(choice) < len(archives) and username != '':
                filename = archives[choice] + '_' + username + '_' + str(get_timestamp()) + '.zip'
                if check_filename(filename):
                    print('开始压缩存档...')
                    zip_archive(archive_name=archives[choice], upload_user=username)
                    print('压缩成功，正在上传至服务器，需要较长时间，请耐心等待...')
                    try:
                        with open(filename, mode='rb') as file:
                            response = requests.post(url=main_url + '/archive_upload/',
                                                     files={'file': file})
                            if 'success' in response.text:
                                print('上传成功！')
                                pause()
                                continue
                            elif 'Error' in response.text:
                                print('上传出错，服务器返回错误信息：{}'.format(response.text))
                                pause()
                            else:
                                print('上传出错，未知错误！')
                                pause()
                    except Exception as e:
                        print('程序出错，请联系开发人员，错误代码如下：{}'.format(e))
                        pause()
        elif int(cmd) == 2:
            clear()
            try:
                response = requests.get(main_url + "/get_archives_info/")
                if 'Error' not in response.text:
                    info = response.json()['info']
                else:
                    print('获取服务器数据出错，错误信息：{}'.format(response.text))
                    pause()
                    continue
            except Exception as e:
                print('获取服务器数据出错，错误信息：{}'.format(e))
                pause()
                continue
            print('当前服务器上有以下存档文件：')
            for index, value in enumerate(info):
                print('{}. 世界名称：{}  上传用户：{}  上传时间：{}'.format(index + 1, value['world_name'], value['upload_user'],
                                                             value['upload_time']))
            choice = int(input('请选择你需要的存档（这将会覆盖你当前本地同名的世界存档，请谨慎选择）：')) - 1
            if choice < len(info):
                try:
                    print('正在从服务器取回存档，这将需要一段时间，请稍后...')
                    response = requests.get(
                        main_url + '/archive_download/{}'.format(info[choice]['archive_name']))
                    with open(info[choice]['archive_name'], mode='wb') as file:
                        file.write(response.content)
                    unzip_archive(info[choice]['archive_name'])
                    print('取回成功！')
                    pause()
                    continue
                except Exception as e:
                    print('从服务器取回存档出现错误，错误信息：{}'.format(e))
                    pause()
                    continue
