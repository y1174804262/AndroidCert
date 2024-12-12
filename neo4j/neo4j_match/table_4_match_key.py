from neo4j import neo4j

driver = neo4j()


def match_Key_type():
    cypher = "MATCH (n:Key) RETURN n"
    result = driver.run(cypher)
    return result


def match_Key_cert(cert_type, Keys):
    """
    MATCH (n:`根证书`)-[:Key]->(n2:Key) where n2.`类型`='RSA' and n2.`长度`=2048 return n
    :param cert_type:
    :return:
    """
    print(f"证书类型：{cert_type}")
    for key in Keys:
        key_type = key['n']['类型']
        key_length = key['n']['长度']
        # cypher = "MATCH (n:`" + cert_type + "`:trust)-[:Key]->(n2:Key) where n2.`类型`='" + key_type + "' and n2.`长度`=" + str(key_length) + " return count(n)"
        cypher = "MATCH (n:`" + cert_type + "`)-[:Key]->(n2:Key) where n2.`类型`='" + key_type + "' and n2.`长度`=" + str(key_length) + "  and not n:trust return count(n)"
        result = driver.run(cypher)
        # print(f"密钥类型：{key_type}({key_length}):{result.data()[0]['count(n)']}")
        print(f"{key_type}({key_length}):{result.data()[0]['count(n)']}")


if __name__ == '__main__':
    key_list = match_Key_type()
    match_Key_cert('根证书', key_list)
    key_list = match_Key_type()
    match_Key_cert('中间证书', key_list)
    key_list = match_Key_type()
    match_Key_cert('终端证书', key_list)
