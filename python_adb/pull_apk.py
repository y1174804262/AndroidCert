import json
import subprocess
import re
import csv

from python_adb.upload_json import save_data_2_json


def get_installed_packages():
    """获取所有已安装的应用包名"""
    result = subprocess.run(['adb', 'shell', 'pm', 'list', 'packages', '-3'], capture_output=True, text=True)
    packages = result.stdout.splitlines()
    package_names = [pkg.split(":")[1] for pkg in packages]
    return package_names


def get_package_file(package_name):
    """
    通过包名获取apk文件路径
    :param package_name: 包名
    :return: apk文件路径
    """
    result = subprocess.run(['adb', 'shell', 'pm', 'path', package_name], capture_output=True, text=True)
    if result.returncode == 0:
        path = result.stdout.strip().split(":")[1]
    return path



def pull_app_apk(package_names):
    """
    通过安装包名，将app下载至本地
    :param package_names: app包名
    """

    apk_cache = "E:\\PythonProject\\All_Android_Certificate_2\\download_cache\\apk_cache\\shouji"
    i = 0                                                         # 默认为0
    for package_name in package_names:
        package_file = get_package_file(package_name)
        i += 1
        new_package_file = package_name + "_" + str(i) + ".apk"
        new_package_path = apk_cache + "\\" + new_package_file
        try:
            result = subprocess.run(['adb', 'pull', package_file, new_package_path], capture_output=True, text=True)
            result.check_returncode()  # 确保命令执行成功
        except Exception as e:
            print(f"Error pulling APK: {e}")
            continue
        app_name, app_activity = get_apk_info(new_package_path)
        # 将信息写入json

        json_data = {
            "app_name": app_name,
            "package_name": package_name,
            "file_name": new_package_file,
            "app_activity": app_activity
        }
        file_path = '../download_cache/apk_json/apk_shouji_1.json'  # 每次替换
        save_data_2_json(json_data, file_path=file_path)
        print(i)
    return


def get_apk_info(apk_path):
    """
    使用 aapt 工具提取 APK 文件的应用名称
    :param apk_path: APK文件路径
    :return: 应用名称
    """
    print(apk_path)

    try:
        result = subprocess.run(['aapt', 'dump', 'badging', apk_path], capture_output=True, text=True, encoding='utf-8')
        result.check_returncode()  # 确保命令执行成功
        if result.stdout:
            app_name = re.findall(r"application-label:'(.*?)'", result.stdout)
            app_activity = re.findall(r"launchable-activity: name='(.*?)'", result.stdout)
            return app_name[0], app_activity[0]
    except Exception as e:
        print(f"Error extracting app info: {e} + {apk_path}")
        return None, None


def main():
    # 获取所有应用包名
    package_names = get_installed_packages()
    # package_names.remove("com.huawei.appmarket")
    # for i in range(0, 12):             # 注意注释
    #     package_names.pop(0)            # 注意注释
    pull_app_apk(package_names)
    print(f"Found {len(package_names)} packages.")


if __name__ == "__main__":
    main()
