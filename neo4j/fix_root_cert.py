import os

from log_config import create_log
from Scan_Certificate.read_android_cert import read_android_cert, parse_certificate
from neo4j import neo4j
from neo4j.get_cert_data import cert_data_parse
log_driver = create_log()
driver = neo4j()


def match_less_node():
    """
    MATCH (n)-[r1:Issuer]->(m) WHERE NOT EXISTS((n)-[:Subject]->()) AND NOT EXISTS((m)-[:father]->()) RETURN n
    MATCH (n:Issuer) WHERE NOT EXISTS(()-[:Subject]->(n)) RETURN n
    检索缺少Subject节点的Issuer节点(这些节点一般是缺少的根证书)
    :return: 返回Issuer节点的CN
    """
    cypher = "MATCH (n:Issuer) WHERE NOT EXISTS(()-[:Subject]->(n)) RETURN n"
    match_issuer_node = driver.run(cypher)
    issuer_nodes = []
    for i in match_issuer_node:
        issuer_nodes.append(i["n"]["CN"])
    return issuer_nodes


def upload_root_cert(issuer_nodes):
    """
    上传缺失的根证书
    :param issuer_nodes: 缺少Subject节点的Issuer节点
    :return:
    """
    file_paths = "../Scan_result/root_cert"
    path = os.listdir(file_paths)
    for file in path:
        if file.endswith(".crt"):
            file_path = os.path.join(file_paths, file)
            cert_data_bytes = read_android_cert(file_path)
            x509 = parse_certificate(cert_data_bytes)
            if x509.get_subject().CN in issuer_nodes:
                # 上传根证书
                cert_data_parse(x509, '根证书', file)
                log_driver.info("补全根证书：" + file)
                print("上传完成")


def connect_father_relation():
    """
    MATCH (n2:`中间证书`), (n1:`根证书`) WHERE NOT EXISTS((n2)-[:father]->()) and exists ((n1)-[:Subject]->()-[:Issuer]->(n2)) RETURN n2, n1
    连接根证书与中间证书的关系
    :return:
    """
    cypher = ("MATCH (n2:`中间证书`), (n1:`根证书`) "
              "WHERE NOT EXISTS((n2)-[:father]->()) "
              "and exists ((n1)-[:Subject]->()-[:Issuer]->(n2)) "
              "RETURN n2, n1")
    match_result = driver.run(cypher)
    for i in match_result:
        cypher = ("MATCH (n1:`根证书`), (n2:`中间证书`) "
                  "WHERE n1.`序列号` = '" + i["n1"]["序列号"] + "' "
                  "and n2.`序列号` = '" + i["n2"]["序列号"] + "' "
                  "CREATE (n2)-[:father]->(n1)")
        driver.run(cypher)
    print("连接完成")


if __name__ == '__main__':
    temp_issuer_nodes = match_less_node()   # 检索缺少Subject节点的Issuer节点
    upload_root_cert(temp_issuer_nodes)     # 上传缺失的根证书
    connect_father_relation()               # 连接根证书与中间证书的关系
