import os
import hashlib

def calculate_md5(file_path, chunk_size=8192):
    """计算文件的MD5值"""
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            md5.update(chunk)
    return md5.hexdigest()

def count_files_by_md5(directory):
    """统计目录中每个文件根据MD5值出现的次数"""
    md5_dict = {}

    # 遍历目录中的所有文件，包括所有子目录
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_md5 = calculate_md5(file_path)

            # 更新MD5值的计数
            if file_md5 in md5_dict:
                md5_dict[file_md5] += 1
            else:
                md5_dict[file_md5] = 1
    return md5_dict


def find_md5(directory):
    md5_value = [        'e357f9241d32446cc1de1888055eae7b',
    ]
    """
        腾讯广告：e.qq.com('78b368b3ce0465f47338adb5933328cb', 1046)     E:\PythonProject\All_Android_Certificate_2\Scan_result\certs\bangongruanjian\aa_94\157.255.220.157_443_8.crt
        个推：getui.com ('14d83941d94b5aae5c035d067b49ead6', 1222)      bangongruanjian\agents_157\101.68.218.163_443_14.crt
        今日头条：pangolin-sdk-toutiao.com('6ca4da56950e3ead5712a3548e5159d2', 1343)     \bangongruanjian\android_206\218.57.18.209_443_13.crt
        火山引擎：volces.com ('bc218b3eb3385fcfcbb65e2dd727c961', 1373)  \bangongruanjian\android_206\27.221.123.183_443_34.crt
        今日头条广告：pangolin-sdk-toutiao1.com ('235ee5def089344992b96960ab31a3d6', 1440)   bangongruanjian\android_206\61.243.15.103_443_22.crt
        中移互联网有限公司：cmpassport.com（手机号登陆）cmpassport.com('0ef1c725932879a5f16e903e7639a1b6', 1447)  bangongruanjian\aivoice_51\112.33.111.251_443_22.crt
        极光推送：jpush.cn ('e3bb329405dc3200d7c3b3264baf3cc0', 1592)    bangongruanjian\aa_94\120.233.114.194_443_16.crt
        百度：baidu.com    ('c8927d275087d3db2fa53a88db9cc866', 1605)      \bangongruanjian\aiqicha_138\163.177.17.119_443_3
        今日头条广告：pglstatp-toutiao.com   ('f3453f2a7c83348c1adba2d13e445564', 1611)  bangongruanjian\android_206\223.109.115.137_443_47.crt
        淘宝：tanx.com ('db91f41165f796b68e76c597e03762f4', 1939)  bangongruanjian\aa_94\203.119.169.41_443_15.crt
        腾讯bugli库：*.jun14-2024-1.ias.qq.com(https://docs.bugly.qq.com/docs/)('91da24d510a674f94900255605036f56', 2292)  bangongruanjian\activity_185\116.162.36.63_443_2.crt_91
        友盟: umeng.com    ('e357f9241d32446cc1de1888055eae7b', 4945)  bangongruanjian\aa_94\223.109.148.139_443_13.crt
    """
    # 遍历目录中的所有文件，包括所有子目录
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_md5 = calculate_md5(file_path)
            if file_md5 in md5_value:
                print(file_path + '_' + file_md5)

def main_count():
    # 运行统计
    directory_path = '../Scan_result/certs'  # 将此路径替换为实际目录路径
    md5_count = count_files_by_md5(directory_path)

    sorted_md5_count = sorted(md5_count.items(), key=lambda item: item[1])

    # # 输出排序后的结果
    # print(sorted_md5_count)
    #

    # 输出统计结果
    for data in sorted_md5_count:
        print(data)

def main_find():
    directory_path = '../Scan_result/certs'
    find_md5(directory_path)

if __name__ == '__main__':
    # main_find()
    main_count()