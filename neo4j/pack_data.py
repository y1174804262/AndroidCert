def pack_node(node_type, node_property):
    """
    封装节点
    :param node_type:  节点类型
    :param node_property:  节点属性
    :return:
    """
    return {
        "node_type": node_type,
        "node_property": node_property
    }
def pack_relation(relation_type, relation_property):
    """
    封装关系
    :param relation_type:  关系类型
    :param relation_property:  关系属性
    :return:
    """
    return {
        "relation_type": relation_type,
        "relation_property": relation_property
    }




