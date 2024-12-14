from neo4j import neo4j

driver = neo4j()


def delete_graph():
    """
    清空图谱
    :return:
    """
    cypher = "MATCH (n) DETACH DELETE n"
    driver.run(cypher)
    print("清空完成")


if __name__ == '__main__':
    delete_graph()


def find_node(node_type, node_property):
    """

    查找节点是否存在，根据是否存在颁发者选择是否需要创建主体节点
    :param node_type:  节点类型
    :param node_property:  节点属性
    :return:
    """
    cypher = "MATCH (node:" + node_type + "{" + node_property + "}) RETURN node"
    print(cypher)
    flag = driver.run(cypher).data()
    if flag:
        return flag
    else:
        return False


def change_node_property_value(node_type, node_property, property_name, property_value):
    """
    修改节点属性值
    :param node_type:  节点类型
    :param node_property:  节点属性
    :param property_name:  属性名
    :param property_value:  属性值
    :return:
    """
    cypher = "MATCH (node:" + node_type + "{" + node_property + "}) SET node." + property_name + ' = "' + property_value + '"'
    print("**************" + cypher)
    driver.run(cypher)


def cypher_creat_cert_node(node_type, node_property):
    """
    创建证书节点，根据证书的序列号创建节点，类型为 Cert、终端证书、中间证书、根证书的子集
    :param node_type:  证书类型
    :param node_property:   证书属性
    :return:
    """
    cypher = "MERGE (node:" + node_type + " {" + node_property + "})"
    print(cypher)
    driver.run(cypher)


def add_type_label(node_type, node_property):
    """
    添加标签
    :param node_type:
    :param node_property:
    :return:
    """
    cypher = "MATCH (node {" + node_property + "}) SET node:" + node_type
    driver.run(cypher)


def create_relation(start_node, end_node, relation):
    # print("MATCH (node1:" + start_node['node_type'] + "{" + start_node['node_property'] + "}),(node2:" + end_node[
    #     'node_type'] + "{" + end_node['node_property'] + "}) MERGE (node1)-[r:" + relation['relation_type'] + "{" +
    #       relation['relation_property'] + "}]->(node2)")
    cypher_relation = (
            "MATCH (node1:" + start_node['node_type'] + "{" + start_node['node_property'] + "}),(node2:" + end_node[
        'node_type'] + "{" + end_node['node_property'] + "}) MERGE (node1)-[r:" + relation['relation_type'] + "{" +
            relation['relation_property'] + "}]->(node2)")
    driver.run(cypher_relation)


def upload_cert(start_node, end_node, relation):
    """
    上传证书数据
    :param start_node: 头节点，类型为字典，有两个字段，node_type和node_property
    :param end_node:  尾节点，类型为字典，有两个字段，node_type和 node_property
    :param relation:  关系，类型为字典，有两个字段，relation_type 和 relation_property
    :return:
    """
    cypher_2 = "MERGE (node2:" + end_node['node_type'] + " {" + end_node['node_property'] + "})"
    cypher_relation = (
            "MATCH (node1:" + start_node['node_type'] + "{" + start_node['node_property'] + "}),(node2:" + end_node[
        'node_type'] + "{" + end_node['node_property'] + "}) MERGE (node1)-[r:" + relation['relation_type'] + "{" +
            relation['relation_property'] + "}]->(node2)")
    driver.run(cypher_2)
    driver.run(cypher_relation)


def upload_cert_chain(son_number, father_number, son_cert_figure, father_cert_figure):
    """
    上传证书链
    :param son_number:  子证书序列号
    :param father_number:  父证书序列号
    :return:
    """
    cypher = 'MATCH (node1:Cert{序列号:"' + son_number + '",Figure:"' + son_cert_figure + '" }),(node2:Cert{序列号:"' + father_number + '",Figure:"' + father_cert_figure + '"}) MERGE (node1)-[r:father{name:"father"}]->(node2)'
    print(cypher)
    driver.run(cypher)

# if __name__ == '__main__':
#     node1_type = 'Cert'
#     node1_property = '序列号:"aaa"'
#     node2_type = 'Version'
#     node2_property = '版本号:"V3"'
#     relations_type = '版本'
#     relations_property = 'name:"版本"'
#     upload_cert(node1_type, node1_property, node2_type, node2_property, relations_type, relations_property)
