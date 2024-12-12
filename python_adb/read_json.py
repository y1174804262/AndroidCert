import json

def read_json(file):
    # 读取 JSON 文件
    with open(file, 'r', encoding='utf-8') as file:
        app_infos = json.load(file)
    return app_infos


if __name__ == '__main__':
    # 读取 JSON 文件
    app_list = read_json('../download_cache/file2app/file2app_music_1.json')
    print(app_list)
