import time

from neo4j import neo4j
import pandas as pd

driver = neo4j()


def match_node_validity(cert_type):
    """
    MATCH (n:`根证书`)-[:Validity]->(n2:Validity) RETURN n2
    查询证书有效期,并统计每个有效期的证书数量
    :param cert_type:
    :return:
    """
    Validity = []
    cypher = "MATCH (n:`" + cert_type + "`:trust)-[:Validity]->(n2:Validity) RETURN n2"
    # cypher = "MATCH (n:`" + cert_type + "`)-[:Validity]->(n2:Validity) where not n:trust RETURN n2"
    result = driver.run(cypher)
    for data in result:
        Validity.append(data['n2']['有效期'])
    return Validity


def main_cert_validity():
    cert_types = ["根证书", "中间证书", "终端证书"]
    # cert_types = ["终端证书"]
    for cert_type in cert_types:
        print("\n\n" + cert_type + "有效期")
        validity = match_node_validity(cert_type)
        series = pd.Series(validity)
        count = series.value_counts()
        sorted_count = count.sort_index()
        for i in sorted_count.index:
            print(i, sorted_count[i])
        # print(sorted_count)


def check_expired_cert():
    """
    MATCH (n:Cert)-[:Validity]->(n1:Validity) WHERE n1.`终止日期` < '20240814' RETURN n
    查询过期证书
    :return:
    """
    # times = time.strftime("%Y-%m-%d", time.localtime())
    times = '2024-08-16'
    cypher = "MATCH (n:Cert:trust)-[:Validity]->(n1:Validity) WHERE n1.`终止日期` < '" + times + "' RETURN n"
    # cypher = "MATCH (n:Cert)-[:Validity]->(n1:Validity) WHERE n1.`终止日期` < '" + times + "' and not n:trust RETURN n"
    print("查询过期证书：")
    print(cypher)
    results = driver.run(cypher)
    for result in results.data():
        try:
            print("序列号：" + result['n']['序列号'] + "证书名称：" + result['n']['证书名称'])
        except TypeError:
            print("序列号：" + result['n']['序列号'] + "证书名称：None")

if __name__ == '__main__':
    main_cert_validity()
    # check_expired_cert()