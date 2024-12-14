import os

from OpenSSL import crypto
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from neo4j import neo4j

driver = neo4j()


def read_android_ca_cert(file):
    with open(file, 'rb') as cert_file:
        cert_data = cert_file.read()
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_data)
    try:
        figure = cert.digest("sha1").decode("utf-8")
        return str(figure)
    except Exception as e:
        if "ExtensionNotFound" in str(e):
            print(f"Extension not found: {file}")


def match_Figure(figure_list):
    node_list = []
    count = 0
    figure_lists = []
    for figure in figure_list:
        # print(cn)
        cypher = "MATCH (n:`根证书`)-[:Subject]->(m) where n.Figure = '" + figure + "' return m, n"
        # print(cypher)
        result = driver.run(cypher)
        temp_data = result.data()
        if temp_data:
            data_temp = temp_data[0]["m"]["CN"]
            data = temp_data[0]["n"]["Figure"]
            cypher = "match p=(n:`终端证书`)-[:father*1..8]->(m:`根证书`) where m.Figure= '" + data + "' return count (n)"
            # print(data)
            result = driver.run(cypher)
            temp_data = result.data()
            print(data_temp)
            print(temp_data[0]["count (n)"])
            node_list.append(data_temp)
            figure_lists.append(figure)
    for node in node_list:
        print(node)
    return figure_lists

if __name__ == '__main__':
    file_name = "../../Scan_result/androidcert"
    android_figure_list = []
    for file in os.listdir(file_name):
        file_path = os.path.join(file_name, file)
        ca_figure = read_android_ca_cert(file_path)
        if ca_figure == "62:52:DC:40:F7:11:43:A2:2F:DE:9E:F7:34:8E:06:42:51:B1:81:18":
            print(file_path)
        if ca_figure is not None and ca_figure not in android_figure_list:
            android_figure_list.append(ca_figure)
    figure_lists = match_Figure(android_figure_list)
    temp_str = ""

    for figure in figure_lists:
        # temp_str = temp_str + 'and not m.Figure= "' + figure + '"'
        temp_str = temp_str + 'or m.Figure= "' + figure + '"'
    # 添加trust
    cypher_trust = 'MATCH p=(:`中间证书`)-[:father*1..6]->(m:`根证书`)-[:Subject]->() where ' + temp_str + ' set m:trust'
    cypher_trust_2 = "match p=(m:Cert)-[:father*1..6]->(n:trust) set m:trust"
    cypher = 'MATCH p=(:`中间证书`)-[:father*1..6]->(m:`根证书`)-[:Subject]->() where  m.Figure = "None" ' + temp_str + ' return p'
    print(cypher)
    print(cypher_trust)
