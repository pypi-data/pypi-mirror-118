# PyNeo
#
# @Author: Lin, Jason
# @Email : Jason.M.Lin@outlook.com
# @Time  : 2021/8/30 5:43 下午
#
# =============================================================================
"""data.py
"""
from __future__ import annotations
from typing import *


class Element(object):
    _labels: Union[List[str], str] = None
    _properties: Optional[Dict[str, Union[str, int]]] = None
    unique: bool = False     # 公共访问权限, 可以随时修改, 配置这个元素默认不能重复创建

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, labels: Union[List[str], str]):
        """至少有一个标签"""
        assert len(labels) >= 1
        if isinstance(labels, str):
            self._labels = [labels]
        elif isinstance(labels, (list, tuple)):
            assert len(labels) >= 1
            for item in labels:
                assert isinstance(item, str)
            self._labels = sorted(labels)
        else:
            raise AssertionError('未知类型')

    @property
    def properties(self):
        return self._properties

    @properties.setter
    def properties(self, properties: Dict[str, Union[str, int]]):
        """排序后的字典"""
        keys = sorted(properties)
        res = {key: properties[key] for key in keys}
        self._properties = res

    def __hash__(self):
        """作为唯一性校验使用"""
        if self.unique:
            res = hash(self)
        else:
            res = hash(str(self))
        return res

    def __eq__(self, other):
        return isinstance(other, Element) and hash(self) == hash(other)


class Node(Element):
    def __init__(self, *labels, **properties):
        """在属性中添加unique=True, 令当前实例唯一"""
        self.labels = labels
        if 'unique' in properties:
            self.unique = bool(properties.pop('unique'))
        self.properties = properties

        # TODO: 是否匹配
        # if str(self) == "Node(:Temperature {'data': 'Cool', 'name': 'Temperature'})":
        #     raise ValueError

    def __repr__(self):
        labels = ':' + ':'.join(self._labels)
        if self._properties:
            res = f'Node({labels} {self._properties})'
        else:
            res = f'Node({labels})'
        return res


class Relationship(Element):
    _start: Node = None
    _end: Node = None

    def __init__(self, start: Node, labels: Union[List[str], str], end: Node, **properties):
        """在属性中添加unique=True, 令当前实例唯一"""
        self.start = start
        self.labels = labels
        self.end = end

        if 'unique' in properties:
            self.unique = bool(properties.pop('unique'))
        self.properties = properties

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, node: Node):
        assert isinstance(node, Node)
        self._start = node

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, node: Node):
        assert isinstance(node, Node)
        self._end = node

    def __repr__(self):
        labels = ':' + ':'.join(self._labels)
        if self._properties:
            res = f'({self._start})-[{labels} {self._properties}]->({self._end}))'
        else:
            res = f'({self._start})-[{labels}]->({self._end}))'
        return res


class Subgraph(object):
    _nodes: List[Node] = None
    _relationships: Optional[List[Relationship]] = None

    def __init__(self, nodes: List[Node], relationships: Optional[List[Relationship]] = None):
        self.nodes = nodes
        self.relationships = relationships

    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, nodes):
        assert isinstance(nodes, list) and len(nodes) > 0
        for item in nodes:
            assert isinstance(item, Node)
        self._nodes = list(set(nodes))

    @property
    def relationships(self):
        return self._relationships

    @relationships.setter
    def relationships(self, relationships):
        if relationships:
            assert isinstance(relationships, list)
            for item in relationships:
                assert isinstance(item, Relationship)
            self._relationships = list(set(relationships))
        else:
            self._relationships = []

    @property
    def cql(self):
        """
        把subgraph转化为cql语句
        """
        cql_list = []
        node_dict = {}
        for i in range(len(self.nodes)):
            node = self.nodes[i]
            node_id = f'node_{i}'

            labels = ''
            for label in node.labels:
                labels += f':{label}'

            if not node.properties:
                cql = f"create ({node_id}{labels})"
            else:
                properties = []
                for key, value in node.properties.items():
                    properties.append(f"{key}:'{value}'")
                properties = ', '.join(properties)
                cql = f"create ({node_id}{labels} {{{properties}}})"
            cql_list.append(cql)
            node_dict[self.nodes[i]] = node_id
        if self.relationships:
            cql_relations = []
            for relationship in self.relationships:
                start_node_id = node_dict[relationship.start]
                end_node_id = node_dict[relationship.end]

                labels = ''
                for label in relationship.labels:
                    labels += f':{label}'

                if not relationship.properties:
                    cql = f"({start_node_id})-[{labels}]->({end_node_id})"
                else:
                    properties = []
                    for key, value in relationship.properties.items():
                        properties.append(f"{key}:'{value}'")
                    properties = ', '.join(properties)
                    cql = f"({start_node_id})-[{labels} {{{properties}}}]->({end_node_id})"
                cql_relations.append(cql)
            cql_relations = 'create\n' + ',\n'.join(cql_relations)
            cql_list.append(cql_relations)
        cql = '\n'.join(cql_list)
        return cql

    def distinct(self):
        self._nodes = list(set(self._nodes))
        self._relationships = list(set(self._relationships))

    def __or__(self, other):
        n = list(set(self.nodes) | set(other.nodes))
        r = list(set(self.relationships) | set(other.relationships))
        return Subgraph(n, r)

    def __and__(self, other):
        n = list(set(self.nodes) & set(other.nodes))
        r = list(set(self.relationships) & set(other.relationships))
        return Subgraph(n, r)

    def __sub__(self, other):
        n = list(set(self.nodes) - set(other.nodes))
        r = list(set(self.relationships) - set(other.relationships))
        return Subgraph(n, r)

    def __add__(self, other: Subgraph):
        self._nodes.extend(other.nodes)
        self._relationships.extend(other.relationships)
        return self

    def __xor__(self, other):
        n = list(set(self.nodes) ^ set(other.nodes))
        r = list(set(self.relationships) ^ set(other.relationships))
        return Subgraph(n, r)

