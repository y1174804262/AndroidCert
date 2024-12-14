from neo4j import neo4j

driver = neo4j()


def match_Signature_type():
    cypher = "MATCH (n:SignatureAlgorithm) RETURN n"
    result = driver.run(cypher)
    return result


def match_Signature_cert(cert_type, signatures):
    print(f"证书类型：{cert_type}")
    for signature in signatures:
        signature_value = signature['n']['签名算法']
        # cypher = "MATCH (n:`" + cert_type + "`:trust)-[:SignatureAlgorithm]->(n2:SignatureAlgorithm) where n2.`签名算法`='" + signature_value + "'return count(n)"
        cypher = "MATCH (n:`" + cert_type + "`)-[:SignatureAlgorithm]->(n2:SignatureAlgorithm) where n2.`签名算法`='" + signature_value + "' and not n:trust return count(n)"
        result = driver.run(cypher)
        # print(f"签名算法类型：{signature_value}:{result.data()[0]['count(n)']}")
        print(f"{signature_value}:{result.data()[0]['count(n)']}")


if __name__ == '__main__':
    signature_list = match_Signature_type()
    match_Signature_cert('根证书', signature_list)
    signature_list = match_Signature_type()
    match_Signature_cert('中间证书', signature_list)
    signature_list = match_Signature_type()
    match_Signature_cert('终端证书', signature_list)
