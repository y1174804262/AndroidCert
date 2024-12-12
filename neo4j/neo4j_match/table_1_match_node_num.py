from neo4j import neo4j

driver = neo4j()


def match_node_num(node_type):
    """
    查询节点数量
    :return:
    """
    cypher = "MATCH (n: `" + node_type + "`) RETURN count(DISTINCT n) as count"
    # cypher = "MATCH (n:trust: `" + node_type + "`) RETURN count(DISTINCT n) as count"
    # cypher = "MATCH (n: `" + node_type + "`) where not n:trust RETURN count(DISTINCT n) as count"
    result = driver.run(cypher)
    return result.data()[0]['count']

def match_no_father_cert():
    """
    查询没有父节点的证书
    match (n:`中间证书`) where not (n)-[:father]->() return n
    :return:
    """
    cypher = "match (n:`中间证书`) where not (n)-[:father]->() return count(distinct(n))"
    result = driver.run(cypher)
    print("没有父节点的中间证书数量: ", result.data()[0]['count(distinct(n))'])
    cypher = "match (n:`终端证书`) where not (n)-[:father]->() return count(distinct(n))"
    result = driver.run(cypher)
    print("没有父节点的终端证书数量: ", result.data()[0]['count(distinct(n))'])

if __name__ == '__main__':
    root_cert_num = match_node_num("根证书")
    middle_cert_num = match_node_num("中间证书")
    terminal_cert_num = match_node_num("终端证书")
    all_cert_num = root_cert_num + middle_cert_num + terminal_cert_num
    print("根证书数量: ", root_cert_num, "所占比例: ", root_cert_num / all_cert_num*100, "%")
    print("中间证书数量: ", middle_cert_num, "所占比例: ", middle_cert_num / all_cert_num*100, "%")
    print("终端证书数量: ", terminal_cert_num, "所占比例: ", terminal_cert_num / all_cert_num*100, "%")
    match_no_father_cert()