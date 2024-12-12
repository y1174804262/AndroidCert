import json
import os


def save_data_2_json(app_data, file_path='../download_cache/apk_music_2.json'):
    # 检查文件是否存在
    if os.path.exists(file_path):
        # 如果文件存在，加载现有数据
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                apps_data = json.load(file)
            except json.JSONDecodeError:
                # 如果文件损坏或为空，初始化为空列表
                apps_data = []
    else:
        # 如果文件不存在，初始化为空列表
        apps_data = []

    # 将新的数据添加到列表中
    apps_data.append(app_data)

    # 将更新后的数据写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(apps_data, file, ensure_ascii=False, indent=4)


# 示例应用数据
app_data = {
    "app_name": "恩雅音乐",
    "package_name": "com.enya.enyamusic",
    "file_name": "com.enya.enyamusic_1.apk",
    "app_activity": "com.enya.enyamusic.view.activity.start.SplashActivity"
}
