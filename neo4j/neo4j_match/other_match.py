from neo4j import neo4j

driver = neo4j()


def match_app():
    cypher = "MATCH (n:APP) RETURN count(DISTINCT n) as count"
    result = driver.run(cypher)
    print("App数量: ", result.data())

    cypher = "MATCH (n) WHERE EXISTS(n.`APP类型`) RETURN DISTINCT n.`APP类型`"
    result = driver.run(cypher)
    app_type_list = []
    for data in result:
        app_type_list.append(data['n.`APP类型`'])
    print("App类型数量: ", len(app_type_list))
    print("App类型: ", app_type_list)
    # 每个类型的APP数量
    for app_type in app_type_list:
        cypher = "MATCH (n:APP) WHERE n.`APP类型`='" + app_type + "' RETURN count(n) as count"
        result = driver.run(cypher)
        print(app_type, "数量: ", result.data()[0]['count'])


def match_repeat_cert():
    cypher = "MATCH (n:`终端证书`) WHERE n.证书名称 IS NOT NULL WITH n,size([x IN split(n.证书名称, ',') WHERE x ENDS WITH '.crt']) AS crtCount RETURN crtCount"
    result = driver.run(cypher)
    count = 0
    count_num = 0
    for data in result:
        print(data['crtCount'])
        if data['crtCount'] > 1:
            count += 1
            count_num += data['crtCount']
    print("重复证书数量: ", count)
    print("重复证书总数: ", count_num)


if __name__ == '__main__':
    match_app()
    # match_repeat_cert()