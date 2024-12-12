# 暂时的测试。后续再考虑怎么做
import os
import time
from Scan_Certificate.parse_cert_plus import *
from Scan_Certificate.read_android_cert import parse_certificate, read_android_cert
from Scan_Certificate.resolve_certchain import *
from Scan_Certificate.store_root_midm_cert import store_cert
from neo4j.pack_data import *
from neo4j.upload import *
from cert_chain_resolver.api import resolve
from python_adb.read_json import read_json


# file2app = read_json("../download_cache/file2app/file2app_music_1.json")


def creat_subject_all(node1_type, node1_property, user_info):
    """
    创建证书的Subject节点,以及展开值的节点
    :param node1_type:  Subject节点类型
    :param node1_property:  Subject节点属性
    :param user_info:  Subject节点的信息
    :return:
    """
    if node1_type == "Subject" or node1_type == "Issuer":
        temp_list = ['C', 'ST', 'L', 'O', 'OU']
        for node in temp_list:
            node2_property = ''
            node2_type = node
            if node == 'ST':
                node2_property = '省州:"' + str(user_info['ST']) + '"'
            elif node == 'C':
                node2_property = '国家:"' + str(user_info['C']) + '"'
            elif node == 'L':
                node2_property = '城市:"' + str(user_info['L']) + '"'
            elif node == 'O':
                node2_property = '组织:"' + str(user_info['O']) + '"'
            elif node == 'OU':
                node2_property = '组织单位:"' + str(user_info['OU']) + '"'
            start_node_data = pack_node(node1_type, node1_property)
            end_node_data = pack_node(node2_type, node2_property)
            node_relation = pack_relation(node, 'name:"' + node + '"')
            upload_cert(start_node_data, end_node_data, node_relation)


def creat_single_node(cert_data, cert_node_data):
    """
    创建证书的单节点,包括版本号，签名算法，有效期
    :param cert_data:  证书数据
    :param cert_node_data:  证书节点数据
    :return:
    """
    # 创建与证书关联的单节点
    creat_list = ['Version', 'SignatureAlgorithm', 'Validity']
    # 创建单节点与关系
    for node in creat_list:
        node2_type = node
        node2_property = ''
        if node == 'Version':
            node2_property = '版本号:"' + str(cert_data.get_version()) + '"'
        elif node == 'SignatureAlgorithm':
            node2_property = '签名算法:"' + str(cert_data.get_signature_algorithm().decode()) + '"'
        elif node == 'Validity':
            start_time_obj, end_time_obj, vila_time = parse_date(cert_data)
            node2_property = ('起始日期:"' + str(start_time_obj) +
                              '",终止日期:"' + str(end_time_obj) +
                              '",有效期:' + str(vila_time))
        start_node_data = cert_node_data
        end_node_data = pack_node(node2_type, node2_property)
        node_relation = pack_relation(node, 'name:"' + node + '"')
        upload_cert(start_node_data, end_node_data, node_relation)


def complex_node_handle(cert_node_data, node2_type, node2_property, node):
    """
    创建证书的多节点类型节点中间代码处理,包括如Subject,Key,Issuer
    主要对要上传的节点包装为头节点，关系，尾节点，包装完成后进行上传
    :param cert_node_data:
    :param node2_type:
    :param node2_property:
    :param node:
    :return:
    """
    if node == 'Issuer':
        node_relation = pack_relation('Issuer', 'name:"Issuer"')
        # 先创建颁发者主体的节点
        cypher_creat_cert_node(node2_type, node2_property)
        create_relation(pack_node(node2_type, node2_property), cert_node_data, node_relation)
        add_type_label("Issuer", node2_property)
    else:
        start_node_data = cert_node_data
        end_node_data = pack_node(node2_type, node2_property)
        node_relation = pack_relation(node, 'name:"' + node + '"')
        upload_cert(start_node_data, end_node_data, node_relation)


def creat_complex_node(cert_data, cert_node_data):
    """
    创建证书的多节点类型的节点,包括如Subject,Key,Issuer
    :param cert_data:  证书数据
    :param cert_node_data:  证书节点数据
    :return:
    """
    complex_list = ['Subject', 'Key', 'Issuer']
    for node in complex_list:
        node2_type = node
        if node == 'Subject':
            subject_info = parse_subject(cert_data)
            # 检查是否存在一个颁发者与证书的Subject相同的证书
            node_type = 'Issuer'
            node_property = 'CN:"' + str(subject_info['CN']) + '"'
            if find_node(node_type, node_property):
                # 如果主体已经被创建为颁发者，则直接创建关系，并为颁发者创建一个Subject的类型
                node_relation = pack_relation('Subject', 'name:"Subject"')
                create_relation(cert_node_data, pack_node(node_type, node_property), node_relation)
                add_type_label("Subject", node_property)
            else:
                # 如果主体没有被创建为颁发者，则创建主体节点
                node2_property = 'CN:"' + str(subject_info['CN']) + '"'
                complex_node_handle(cert_node_data, node2_type, node2_property, node)
                creat_subject_all(node2_type, node2_property, subject_info)
        elif node == 'Issuer':
            issuer_info = parse_issuer(cert_data)
            node2_property = 'CN:"' + str(issuer_info['CN']) + '"'
            complex_node_handle(cert_node_data, node, node2_property, node)
            creat_subject_all(node2_type, node2_property, issuer_info)
        elif node == 'Key':
            key_length, key_type = parse_key(cert_data)
            node2_property = '长度:' + str(key_length) + ',类型:"' + str(key_type) + '"'
            complex_node_handle(cert_node_data, node2_type, node2_property, node)


def parse_app_file(file):
    app_file = file.split('/')[2]
    app_type = app_file.split('\\')[1]
    app_name = file2app[0][app_file.split('\\')[2]]
    cert_file_name = app_file.split('\\')[1] + "-" + app_file.split('\\')[2] + "-" + app_file.split('\\')[3]
    return app_type, app_name, cert_file_name


def cert_data_parse(cert_data, cert_type, cert_file_path=None):
    # 创建证书节点
    node1_type = 'Cert:' + cert_type
    serial_number = parse_serial_number(cert_data)
    if cert_type == '终端证书':
        app_type, app_name, file_name = parse_app_file(cert_file_path)
        # 证书的属性
        node1_property = '序列号:"' + str(serial_number) + '"'  # 证书的节点和属性

        # 创建证书的节点前，先判断下该证书节点是否存在，如果不存在则直接创建，存在可能为共有节点，修改其属性
        temp_node = find_node(node1_type, node1_property)
        if not temp_node:
            node1_property = node1_property + ',' + '证书名称:"' + file_name + '"'
            cypher_creat_cert_node(node1_type, node1_property)  # 创建证书的节点
        else:
            node1_property = '序列号:"' + str(serial_number) + '"'
            node_property_name = '证书名称'
            node_property_value = temp_node[0]['node'][node_property_name]
            node_property_new_value = node_property_value + ',' + file_name
            change_node_property_value(node1_type, node1_property, node_property_name, node_property_new_value)
            node1_property = node1_property + ',' + '证书名称:"' + node_property_new_value + '"'

        # 为终端证书所属APP以及APP所属用户创建节点及关系
        start_node_data = pack_node(node1_type, node1_property)
        end_node_data = pack_node('APP', 'APP名称:"' + app_name + '",APP类型:"' + app_type + '"')
        app_relation = pack_relation('APP', 'name:"APP"')
        upload_cert(start_node_data, end_node_data, app_relation)
    else:
        node1_property = '序列号:"' + str(serial_number) + '"'
        cypher_creat_cert_node(node1_type, node1_property)  # 创建证书的节点

    cert_node_data = pack_node(node1_type, node1_property)
    # 创建与证书关联的单节点
    creat_single_node(cert_data, cert_node_data)
    # 处理多节点与关系
    creat_complex_node(cert_data, cert_node_data)

    return serial_number


def find_cert(file_path):
    try:
        cert_chain = []
        cert_data_bytes = read_android_cert(file_path)
        cert_chain = [split_cert_chain(cert_data_bytes)[0]]
        chain_length = cert_chain.__len__() - 1
        last_cert = cert_chain.pop(chain_length)
        cert_chain = cert_chain + resolve(last_cert)  # 利用所解得的最后一个证书去计算AIA
        cert_chain = list(dict.fromkeys(cert_chain))  # 去重
        x509 = parse_certificate(cert_chain[0])
        cert_chain.pop(0)
        son_cert_serial_number = ""
        father_cert_serial_number = ""
        son_cert_serial_number = cert_data_parse(x509, '终端证书', file_path)
        for cert in cert_chain:
            x509 = parse_certificate(cert)
            # 检查得到的证书是不是根证书
            if x509.get_subject().CN == x509.get_issuer().CN:
                father_cert_serial_number = cert_data_parse(x509, '根证书')
                store_path = "../Scan_result/collect_root_cert/" + father_cert_serial_number + ".crt"
                store_cert(store_path, cert)
            else:
                father_cert_serial_number = cert_data_parse(x509, '中间证书')
                store_path = "../Scan_result/collect_mid_cert/" + father_cert_serial_number + ".crt"
                store_cert(store_path, cert)
            upload_cert_chain(son_cert_serial_number, father_cert_serial_number)  # 链接证书链
            son_cert_serial_number = father_cert_serial_number
    except Exception as e:
        print(f"错误原因：{e},错误位置：{file_path}")


def get_file2app(cert_type):
    _file2app = read_json("../download_cache/file2app/file2app_apk_" + cert_type + "_1.json")
    return _file2app


if __name__ == '__main__':
    time_1 = time.time()
    certs_list_path = "../Scan_result/certs"
    for _certs_path in os.listdir(certs_list_path):  # 软件类型
        cert_path = os.path.join(certs_list_path, _certs_path)
        # 在此定义全局变量file2app
        file2app = get_file2app(_certs_path)
        for _cert in os.listdir(cert_path):  # 软件名称
            app_cert_file = os.path.join(cert_path, _cert)
            # app_cert_file = "../Scan_result/certs\\tuxiangmeihua\\activity_77"

            for cert_file in os.listdir(app_cert_file):  # 证书名称
                all_file_path = os.path.join(app_cert_file, cert_file)
                find_cert(all_file_path)

    print("Time:", time.time() - time_1)
    # print(data)
