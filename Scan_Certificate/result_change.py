"""
删除文件夹中重复证书
"""
import os
import hashlib
from log_config import create_log
from python_adb.read_json import read_json

log_driver = create_log()


def calculate_md5(file_path, chunk_size=8192):
    """Calculate the MD5 checksum of a file."""
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            md5.update(chunk)
    return md5.hexdigest()


def find_and_delete_duplicates(folder_path):
    """Find and delete duplicate files in the given folder based on MD5 checksum."""
    md5_dict = {}
    duplicates = []
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_md5 = calculate_md5(file_path)

            if file_md5 in md5_dict:
                duplicates.append(file_path)
            else:
                md5_dict[file_md5] = file_path

    for duplicate in duplicates:
        os.remove(duplicate)
        print(f"Deleted duplicate file: {duplicate}")


def delete_repeat_files(folder_path):
    """
    删除重复文件
    :param folder_path: 文件夹路径
    :return:
    """
    for folder in os.listdir(folder_path):
        new_path = os.path.join(folder_path, folder)
        find_and_delete_duplicates(new_path)
    print("剔除重复文件完成")


def delete_empty_files(folder_path):
    """
    删除指定目录中的空文件。

    :param folder_path: 要检查的目录路径
    """
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            # 检查文件是否为空
            if os.path.isfile(file_path) and os.path.getsize(file_path) == 0:
                print(f"删除空文件: {file_path}")
                os.remove(file_path)


def delete_empty_folders(folder_path):
    """
    删除指定目录中的空文件夹。
    :param folder_path: 要检查的目录路径
    """
    file2app_path = "../download_cache/file2app"
    file_name = folder_path.split("\\")[-1]
    file2app = []
    for file in os.listdir(file2app_path):
        if file_name in file:
            file2app = read_json(f"{file2app_path}/{file}")
            break
    for root, dirs, _ in os.walk(folder_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if dir == "MobileKTV_12":
                print(dir_path)
            # 检查文件夹是否为空
            if os.path.isdir(dir_path) and not os.listdir(dir_path):
                dir_name = dir_path.split("\\")[-1]
                app_name = file2app[0].get(dir_name)
                log_driver.info(f"没有提取到_{app_name}_的证书")
                os.rmdir(dir_path)


# 剔除干扰文件
def delete_interference_files(folder_path):
    # 先将干扰文件md5值存入列表
    interference_md5 = []
    for file in os.listdir('../Scan_result/interfere/all'):
        file_path = os.path.join('../Scan_result/interfere/all', file)
        file_md5 = calculate_md5(file_path)
        interference_md5.append(file_md5)
    # 遍历证书文件夹，删除干扰文件
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_md5 = calculate_md5(file_path)
            if file_md5 in interference_md5:
                os.remove(file_path)
                log_driver.info(f"Deleted interference file: {file_path}")
                print(f"Deleted interference file: {file_path}")
    print("剔除干扰文件完成")


if __name__ == "__main__":
    _paths = "../Scan_result/certs\\shouji"
    delete_empty_files(_paths)
    delete_repeat_files(_paths)  # 删除重复文件
    delete_empty_folders(_paths)  # 删除空文件夹
    delete_interference_files(_paths)  # 剔除干扰文件
    breakpoint()
    print("hhh")


    _folder_path = "../Scan_result/certs/erci"
    _cert_paths = "../Scan_result/certs"
    # 剔除干扰中重复的证书
    delete_repeat_files('../Scan_result/interfere')
    # 检查干扰证书
    # 检查每个文件夹中的每一个证书，剔除内部重复证书
    # for cert_path in os.listdir(_cert_paths):
    #     _paths = os.path.join(_cert_paths, cert_path)
    #     delete_repeat_files(_paths)  # 删除重复文件
    #     delete_empty_files(_paths)  # 删除空文件
    #     delete_empty_folders(_paths)  # 删除空文件夹
    #     delete_interference_files(_paths)   # 剔除干扰文件
    # 删除空文件
    # 剔除剩余证书中的干扰证书
    # 遍历所有证书，检查出证书中重复最多的证书，按照顺序排列，最好存入文件夹
    delete_repeat_files(_folder_path)  # 删除重复文件
    delete_interference_files(_folder_path)  # 删除干扰文件
    delete_empty_folders(_folder_path)  # 删除空文件夹
    delete_empty_files(_folder_path)  # 删除空文件
