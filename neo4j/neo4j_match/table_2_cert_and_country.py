"""
查询证书主体中的国家, 并统计每个国家的证书数量,排除CN为None的证书
查询CN为None的证书可使用：match (n:Subject) where n.CN='None' return n
"""
from neo4j import neo4j

driver = neo4j()


def match_all_country():
    """
    查询证书主体中的国家
    :return: list 国家列表
    """
    cypher = "MATCH p=(n)-[:Subject]->(n1)-[r:C]->(n2) where not n1.CN = 'None' and not n:trust  RETURN distinct n2"
    result = driver.run(cypher)
    country_list = []
    for data in result:
        country_list.append(data['n2']['国家'])
    return country_list

def match_country(cert_type):
    """
    MATCH p=(n:`中间证书`)-[:Subject]->(n1)-[r:C]->(n2) where not n1.CN = 'None'  RETURN p
    查询证书主体中的国家
    :return: list 国家列表
    """
    # cypher = "MATCH p=(n:`" + cert_type + "`:trust)-[:Subject]->(n1)-[r:C]->(n2) RETURN distinct n2"
    cypher = "MATCH p=(n:`" + cert_type + "`)-[:Subject]->(n1)-[r:C]->(n2) where not n:trust RETURN distinct n2"
    result = driver.run(cypher)
    country_list = []
    for data in result:
        country_list.append(data['n2']['国家'])
    return country_list


def match_country_num(cert_type, country_list):
    """
    查询证书主体中的国家数量
    :return: int 国家所有证书数量
    MATCH p=(n:`" + cert_type + "`)-[:Subject]->(n1)-[r:C]->(n2) WHERE n2.国家='"
                  + country + "' and not n1.CN = 'None' RETURN count(n2) as count
    """
    for country in country_list:
        # 仅搞可信证书
        # cypher = ("MATCH p=(n:`" + cert_type + "`:trust)-[:Subject]->(n1)-[r:C]->(n2) WHERE n2.国家='"
        #           + country + "' RETURN count(distinct n) as count")

        cypher = ("MATCH p=(n:`" + cert_type + "`)-[:Subject]->(n1)-[r:C]->(n2) WHERE n2.国家='"
                  + country + "' and not n:trust RETURN count(distinct n) as count")
        # print(cypher)
        result = driver.run(cypher)
        print(country, " ", result.data()[0]['count'])



def new_country_match():
    cypher = "match (n:`根证书`:trust)-[:Subject]->(p) return p"
    result = driver.run(cypher)
    CN_list = set()
    for data in result:
        CN_list.add(data['p']['CN'])
    for CN in CN_list:
        cypher = "match (m:`终端证书`)-[:father*1..6]->(n:`根证书`:trust)-[:Subject]->(p) where p.CN='" + CN + "'  return count(distinct n),count(distinct m)"
        result = driver.run(cypher)
        data = result.data()
        print(CN, ": ", data[0]['count(distinct n)'], ":", data[0]['count(distinct m)'])

if __name__ == '__main__':
    # countrys = new_country_match()
    cert_types = ["Cert", "根证书", "中间证书", "终端证书"]
    # cert_types = ["终端证书"]
    for cert_type in cert_types:
        print("\n\n" + cert_type + "数量")
        countrys = match_country(cert_type)
        match_country_num(cert_type, countrys)
