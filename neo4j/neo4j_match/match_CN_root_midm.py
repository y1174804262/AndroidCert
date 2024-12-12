from neo4j import neo4j
import pandas as pd

driver = neo4j()

def match_node_1():
    """
    检索根证书，检索每个根证书签发的终端证书的数量,结果以根证书的CN值与终端证书数量为键值对

    :return:
    """
    cypher = "MATCH (n)-[r:Subject]->(n2) where n:`根证书` RETURN n2"
    result = driver.run(cypher)
    CN_list = []
    for data in result:
        CN_list.append(data['n2']['CN'])
    CN_list = list(set(CN_list))
    for CN in CN_list:
        cypher = "MATCH p=(n2:`终端证书`)-[:father*1..6]->(n:`根证书`)-[:Subject]->(n3) where n3.CN ='" + CN + "' AND ALL(node IN nodes(p) WHERE size([x IN nodes(p) WHERE x = node]) = 1) RETURN count(DISTINCT n2) as count"
        result = driver.run(cypher)
        print(CN, "签发的终端证书数量: ", result.data()[0]['count'])



def match_node():
    """
    检索根证书，检索每个根证书签发的终端证书的数量
    :return:
    """
    cypher = "MATCH (n:`终端证书`)-[:father*1..6]->(n2:`根证书`) RETURN n2.`序列号`,count(n) as count"
    result = driver.run(cypher)
    root_cert_list = []
    count_list = []
    for data in result:
        root_cert_list.append(data['n2.`序列号`'])
        count_list.append(data['count'])
        print(data['n2.`序列号`'], "签发的终端证书数量: ", data['count'])
    return root_cert_list, count_list




def match_node_CN(cert_flag):
    """
    查询证书主体中的CN
    :param cert_flag: 取值0,1,2,分别代表全部CA证书,根证书,中间证书
    :return:
    """
    if cert_flag == 0:
        cypher = "MATCH (n)-[r:Subject]->(n2) where n:`根证书` or n:`中间证书`  RETURN n2"
    elif cert_flag == 1:
        cypher = "MATCH (n)-[r:Subject]->(n2) where n:`根证书` RETURN n2"
    elif cert_flag == 2:
        cypher = "MATCH (n)-[r:Subject]->(n2) where n:`中间证书` RETURN n2"
    result = driver.run(cypher)
    CN_list = []
    for data in result:
        CN_list.append(data['n2']['CN'])
    return CN_list


def match_rootCN_leaf_cert(CN_list, cert_flag=1):
    """
    查询根证书签发的终端证书数量，该数量会大于实际证书数量，因为有些终端证书可解析到多个根证书
    :param CN_list:
    :return:
    """
    for CN in CN_list:
        if cert_flag == 1:
            cypher = "MATCH p=(n2:`终端证书`)-[:father*1..6]->(n:`根证书`)-[:Subject]->(n3) where n3.CN ='" + CN + "' AND ALL(node IN nodes(p) WHERE size([x IN nodes(p) WHERE x = node]) = 1) RETURN count(DISTINCT n2) as count"
            # print(cypher)
        elif cert_flag == 2:
            cypher = 'MATCH (n2:`终端证书`)-[:father*1..6]->(n:`中间证书`)-[:Subject]->(n3) where n3.CN ="' + CN + '" RETURN count(DISTINCT n2) as count'
        result = driver.run(cypher)
        print(CN, "签发的终端证书数量: ", result.data()[0]['count'])


def match_node_root():
    """
    MATCH (n:`根证书`) RETURN n.`序列号`
    查询根证书的序列号
    :return:
    """
    cypher = "MATCH (n:`根证书`) RETURN n.`序列号`"
    result = driver.run(cypher)
    root_cert_list = []
    for data in result:
        root_cert_list.append(data['n.`序列号`'])
    return root_cert_list


def match_root_sign_leaf_cert(root_cert_list):
    """
    MATCH (n2:`终端证书`)-[:father*1..6]->(n:`根证书`) where n.`序列号` = 0x214324 RETURN count(n2) as count
    查询根证书签发的终端证书数量
    :return:
    """
    for root_cert in root_cert_list:
        cypher = (
                "MATCH (n2:`终端证书`)-[:father*1..6]->(n:`根证书`) where n.`序列号` ='" + root_cert + "'RETURN count(DISTINCT n2) as count")
        result = driver.run(cypher)
        print(root_cert, "签发的终端证书数量: ", result.data()[0]['count'])


if __name__ == '__main__':
    print("根证书签发的终端证书数量")
    CN_list = match_node_CN(cert_flag=1)
    CN_list = list(set(CN_list))
    match_rootCN_leaf_cert(CN_list, cert_flag=1)
    print("\n中间证书签发的终端证书数量")
    CN_list = match_node_CN(cert_flag=2)
    CN_list = list(set(CN_list))
    match_rootCN_leaf_cert(CN_list, cert_flag=2)
    _root_cert = match_node_root()
    match_root_sign_leaf_cert(_root_cert)
