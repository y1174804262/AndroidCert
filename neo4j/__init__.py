from py2neo import Graph, Node


def neo4j():
    neo_driver = Graph("http://localhost:7474", auth=("neo4j", "123"))
    print("neo4j连接成功！")
    return neo_driver