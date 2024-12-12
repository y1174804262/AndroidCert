"""
这个脚本是嗅探网卡中TLS证书的脚本，并将脚本保存至Scan_Certificate/certs目录下
"""
import json
import os
import subprocess
import threading
import time

from OpenSSL import crypto

from python_adb.read_json import read_json


def run_adb():
    subprocess.Popen(['adb', 'devices'])


def run_app(package_name, package_active):
    """
    运行应用
    :param package_name: 应用包名
    :param package_active: 应用启动活动
    :return:
    """
    # 通过 adb shell am start -n 包名/活动名 命令启动应用
    subprocess.Popen(['adb', 'shell', 'am', 'start', '-n',
                      package_name + '/' + package_active])
    print("app已启动")


def stop_app(package_name):
    """
    停止应用
    :param package_name: 应用包名
    :return:
    """
    # 通过 adb shell am force-stop 包名 命令停止应用
    subprocess.Popen(['adb', 'shell', 'am', 'force-stop', package_name])
    print("app已停止")


def run_tshark(interface):
    """
    运行 tshark 命令
    :param interface: 网卡接口
    :return: 返回一个启动的 tshark 进程
    """

    # 启动 tshark 实时捕获
    # 过滤出 TLS 证书，tls.handshake.type == 11 表示 TLS 证书，-T fields -e tls.handshake.certificate 表示只输出证书字段
    process = subprocess.Popen(
        ['tshark',
         '-i', interface,
         '-Y', 'tls.handshake.type == 11',  # 过滤出 TLS 证书
         '-T', 'fields',  # 指定输出格式
         '-e', 'ip.src',  # 源IP地址
         '-e', 'ipv6.src',  # 源IP地址
         '-e', 'tcp.srcport',  # 源端口
         '-e', 'tls.handshake.certificate'  # 证书字段
         ],
        # 将标准输出和标准错误重定向到管道。这样可以在程序运行时读取 tshark 的输出
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        # 以文本模式读取输出
        text=True
    )
    print("tshark 已启动")
    return process


def process_output(process, file_path, max_time=10):
    """
    处理 tshark 的输出
    :param file_path:
    :param process: 启动的 tshark 进程
    :return:
    """
    start_time = time.time()
    i = 1  # 证书编号(后期考虑好后进行修改)！！！
    for line in process.stdout:  # 逐行读取 tshark 的输出
        time_scape = time.time() - start_time
        print(time_scape)
        # if time_scape > max_time:
        #     return
        i = i + 1
        if line.strip():  # 过滤掉空行
            try:
                line = line.strip().replace("\t\t", "\t")
                packet_data = line.strip().split("\t")
                ip_src = packet_data[0].replace(":", "：")
                port = packet_data[1]
                certs_byte = packet_data[2].split(",")
                with open(f'{file_path}/{ip_src}_{port}_{i}.crt', 'ab') as cert_file:
                    pass
                for cert_byte in certs_byte:
                    cert_der = bytes.fromhex(cert_byte)
                    # print("Certificate extracted")
                    # 使用OpenSSL将DER格式的证书转换为X.509对象
                    cert = crypto.load_certificate(crypto.FILETYPE_ASN1, cert_der)
                    # 将X.509对象编码为PEM格式（CRT格式）
                    pem_content = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
                    # 将证书保存到文件
                    with open(f'{file_path}/{ip_src}_{port}_{i}.crt', 'ab') as cert_file:
                        cert_file.write(pem_content)
            except Exception as e:
                print(f"Error decoding certificate: {e}")


def run_once():
    interface = '4'
    process_tshark = run_tshark(interface)
    file_path = '../Scan_result/interfere'
    output_thread = threading.Thread(target=process_output, args=(process_tshark, file_path))
    output_thread.start()


def main():
    """
    主函数
    :return:
    """
    interface = '4'  # 替换为实际的网络接口编号
    app_list = read_json('../download_cache/apk_json/apk_shouji_1.json')  # 每次替换
    # for temp in range(45):                                        # 注意注释
    #     app_list.pop(0)                                           # 注意注释
    run_adb()
    # 先创建应用名称目录 nn01_123
    for app in app_list:
        app_path = app['file_name'].split('.')[-2]
        file_path = f'../Scan_result/certs/shouji/{app_path}'  # 每次替换
        os.makedirs(file_path, exist_ok=True)
        # 获取应用的启动路径
        app_package = app['package_name']
        app_activity = app['app_activity']
        # 运行 tshark 进程
        process_tshark = run_tshark(interface)
        # 运行应用
        run_app(app_package, app_activity)
        try:
            # file_path = '../Scan_result/certs/music/hwyysc_1'
            output_thread = threading.Thread(target=process_output, args=(process_tshark, file_path))
            output_thread.start()
            time.sleep(30)
            print("准备关闭tshark")
            process_tshark.terminate()
            output_thread.join()  # 等待输出线程结束
            print("tshark 已停止")
            stop_app(app_package)
            time.sleep(2)
            print("一个应用已完成")
        except KeyboardInterrupt:
            process_tshark.terminate()


# 测试函数
if __name__ == '__main__':
    main()
    # run_once()
    """
    考虑是否做停止条件
        global i
        while i < 10:
    """
