import os

from read_json import read_json
from upload_json import save_data_2_json


def file2app_json():
    # 读取 JSON 文件
    apk_json_path = '../download_cache/apk_json'
    file2app_path = '../download_cache/file2app'
    for apk_json_file in os.listdir(apk_json_path):
        data_dict = {}
        json_data = read_json(apk_json_path + '/' + apk_json_file)
        for data in json_data:
            file_name = data['file_name'].split('.')[-2]
            data_dict[file_name] = data['app_name']
        save_data_2_json(data_dict, file_path=file2app_path + '/' + 'file2app_' + apk_json_file)


if __name__ == '__main__':
    file2app_json()
