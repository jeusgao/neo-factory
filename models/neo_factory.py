#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-22 15:17:32
# @Author  : Joe Gao (jeusgao@163.com)

import math
from utils import get_name, get_property
from py2neo import (
    Graph,
    Node,
    Relationship,
    Walkable,
    Path,
    walk,
    Schema,
)
from py2neo.matching import (
    NodeMatcher,
    NodeMatch,
    RelationshipMatcher,
    RelationshipMatch,
)

g = Graph(password="joe")


def init_load_csv(fpath, label, index):
    '''[summary]
        Import csv by LOAD CSV FROM ...
        Arguments:
            fpath: {[Str]} -- the file path/url of csv file
                    If load csv file from file system,:
                       the file must copy to folder neo4j/import,
                       the cur path is neo4j/import,
                       the path start with file:/ or file:///

            label: {[Str]}
            index: {[Str]} -- the property name to index on
    '''
    _qry = [
        f'LOAD CSV WITH HEADERS FROM "{pfath}" AS row CREATE (n:{label}) SET n = row',
        f'CREATE INDEX ON :{label}({index})',
    ]

    for _q in _query:
        g.run(_q)

    return f'CSV file {fpath} imported as User Nodes.'


def _a_r_b(a_label, is_r_type, r_type, b_label, conditions, output):
    '''[Cypher scripts initiate]
    [Build a initiative cypher scripts]
    Arguments:
        a_label {[str]} -- [Start node label]
        is_r_type {bool} -- [Is need relationship or not]
        r_type {[str]} -- [The relationship type]
        b_label {[str]} -- [End node label]
        conditions {[str]} -- [where conditions]
        output {[str]} -- [return command]
    Returns:
        [str] -- [return a initiative cypher scripts before the return]
    '''
    cy = f"MATCH (a:{a_label})"
    if r_type and output not in ['CREATE_RELATIONSHIP']:
        cy += f'-[r:{r_type}]-'
    if b_label:
        if is_r_type in ['Y']:
            cy += '-[r]-'
        else:
            cy += ','
        cy += f"(b:{b_label})"
    if conditions:
        cy += f" WHERE {conditions}"

    return cy


def build_cypher(r, action='U'):
    '''[Cypher builder]
    [Build a cypher scripts for run in graph]
    Arguments:
        r {[row]} -- [a row of a dataframe]
    Keyword Arguments:
        action {str} -- [the match action type, U: update, M: match] (default: {'U'})
    Returns:
        [str] -- [return a full cypher scripts for run in graph]
    '''
    output = None if not r.output or not isinstance(r.output, str) and math.isnan(r.output) else r.output
    a_label = None if not r.a_label or not isinstance(r.a_label, str) and math.isnan(r.a_label) else r.a_label
    a_properties = None if not r.a_properties or not isinstance(r.a_properties, str) and math.isnan(r.a_properties) else r.a_properties
    b_label = None if not r.b_label or not isinstance(r.b_label, str) and math.isnan(r.b_label) else r.b_label
    conditions = None if not r.conditions or not isinstance(r.conditions, str) and math.isnan(r.conditions) else r.conditions
    is_r_type = None if not r.is_r_type or not isinstance(r.is_r_type, str) and math.isnan(r.is_r_type) else r.is_r_type
    r_type = None if not r.r_type or not isinstance(r.r_type, str) and math.isnan(r.r_type) else r.r_type
    r_properties = None if not r.r_properties or not isinstance(r.r_properties, str) and math.isnan(r.r_properties) else r.r_properties

    _cy = _a_r_b(
        a_label,
        is_r_type,
        r_type,
        b_label,
        conditions,
        output,
    )

    if action == 'U':
        if output == 'CREATE_NODE':
            _cy = f"CREATE ({a_label}{a_properties})"
        else:
            if output == 'CREATE_RELATIONSHIP':
                _cy += f" CREATE (a)-[:{r_type}{r_properties}]->(b)"
            elif output.startswith('@'):
                _cy += output[1:]
            else:
                _cy += f' RETURN {output}'

    elif action == 'M':
        _cy += f" RETURN {output}"

    else:
        _cy = None

    return _cy


class TransBase(object):
    '''[Base of transactions]
    [include the basic elements for graph transaction]
    '''

    def __init__(self):
        self.tx = g.begin()
        self.schema = Schema(g)
        self.n_matcher = NodeMatcher(g)
        self.r_matcher = RelationshipMatcher(g)

    def commit(self):
        self.tx.commit()


class NeoCreator(TransBase):
    '''
    Extends:
        TransBase
    '''

    def add_node(self, label, **properties):
        '''[summary]
            Create a node.
            Arguments:
                label {[Str]}
                **properties {[dict]} -- [properties set]
        '''
        node = Node(label, **properties)
        self.tx.create(node)

    def add_relationship(self, node_subj, r_type, node_obj):
        '''[summary]
            Add a relationship between to nodes.
            Arguments:
                node_subj {[Node]} -- [The start node of the relationship]
                r_type {[Str]} -- [The type of the relationship]
                node_obj {[Node]} -- [The end node of the relationship]
        '''
        r = Relationship(node_subj, r_type, node_obj)
        self.tx.create(r)

    def create_index(self, label, keys):
        '''[summary]
            Create a schema index for a label and property keys combination.
            Arguments:
                label {[Str]} -- [Label of node]
                keys {[List]} -- [Property names to indexs]
        '''
        self.schema.create_index(label, keys)


class NeoModifier(TransBase):
    '''
    Extends:
        TransBase
    '''

    def update_node(self, node, labels=None, **properties):
        '''[summary]
            update properties of the node.
            Arguments:
                node {[Node]} -- [the node tobe update.]
                labels {[List]} -- [Add multiple labels to node from the iterable labels.]
                **properties {[Dict]} -- [the properties tobe update,
                  or remove the property if value is None.]
        '''
        if labels:
            node.update_labels(labels)
        for k, v in properties:
            node[k] = v
        self.tx.push(node)

    def rm_node(self, node):
        '''[summary]
            Remove a node from graph.
            Arguments:
                node {[Node]} -- []
        '''
        self.tx.delete(node)

    def rm_node_label(self, node, labels):
        '''[summary]
            Remove label(s) from node.
            Arguments:
                node {[Node]} -- []
                labels {[List]} -- []
        '''
        for label in labels:
            if node.has_label(label):
                node.remove_label(label)
        self.tx.push(node)

    def rm_node_all_labels(self, node):
        '''[summary]
            Remove all labels from a node.
            Arguments:
                node {[Node]} -- []
        '''
        node.clear_labels()
        self.tx.push(node)

    def update_relationship_properties(self, r, **properties):
        '''[summary]
            update properties of the node.
            Arguments:
                r {[Relaionship]} -- [the relationship tobe update.]
                **properties {[Dict]} -- [the properties tobe update,
                                          or remove the property if value is None.]
        '''
        for k, v in properties:
            r[k] = v
        self.tx.push(r)

    def separate_relationship(self, r):
        '''[summary]
            Delete the remote relationships that correspond to those in a local subgraph. This leaves any nodes untouched.
            Arguments:
                r {[Subgraph]} -- [a Relationship, or Node other Subgraph]
        '''
        self.tx.separate(r)

    def drop_index(self, label, keys):
        '''[summary]
            Remove label index for a given property key.
            Arguments:
                label {[type]} -- []
                keys {[type]} -- []
        '''
        self.schema.drop_index(label, keys)


class NeoSeeker(TransBase):
    '''
    Extends:
        TransBase
    '''

    def get_nodes(self, label, conditions=None, order_by=None, limit=None):
        '''[summary]
            Get nodes by Nodematcher.
            Arguments:
                label {[Str]}
            Keyword Arguments:
                conditions {[Str]} -- [] (default: {None})
                order_by {[List]} -- [Sort keys, like: ['_.a', "max(_.a, _.b)]"]
                                     (default: {None})
                limit {[Int]} -- [] (default: {None})
        '''
        nodes = self.n_matcher.match(label)
        if conditions:
            nodes = nodes.where(conditions)
        if order_by:
            nodes = nodes.order_by(','.join(order_by))
        if limit and isinstance(limit, int):
            nodes = nodes.limit(limit)
        return nodes

    def get_relationships(self, nodes=None, r_type=None, **properties):
        '''
            Arguments:
                **properties {[]} -- []

            Keyword Arguments:
                nodes {[Sequece/set]} -- [Sequence(like: (a,)) or Set of start and end nodes
                                          (None means any node);
                                          a Set implies a match in any direction.]
                                         (default: {None})
                r_type {[Str]} -- [type of relationship] (default: {None})
            Returns:
                [RelationshipMatch] -- [Iterable relationships]
        '''
        return r_matcher.match(set(user), r_type=r_type, **properties)

    def get_nodes_relationhships_from_RelationshipMatch(self, r_match):
        '''
            Arguments:
                r_match {[RelationshipMatch]} -- []
            Returns:
                [List] -- [Dicts list: {type: node or relationship}]
        '''
        r = []
        for _x in r_match:
            if not _x:
                continue
            r.append({
                's': _x.start_node,
                'r': _x.relationships[0],
                'e': _x.end_node
            })
        return r

    def get_relationship_property(self, r, keys=None):
        '''
            Arguments:
                r {[Relationship]} -- []
            Keyword Arguments:
                keys {[List]} -- [Property names of relationship] (default: {None})
            Returns:
                [Str] -- [Type name of Relationship]
                [List/None] -- [List: Relationship value of keys,
                                None: if keys=None or not len(keys)]
        '''
        p = None
        if keys and len(keys):
            p = [r[k] for k in keys]
        return r.__class__.__name__, p

    def get_indexes(self, label):
        '''[summary]
            Fetch a list of indexed property keys for a label.
            Arguments:
                [Str] -- [Label of node]
            Returns:
                [List] -- [Indexs of a node label]
        '''
        return self.schema.get_indexes(label)

    def get_all_node_labels(self):
        '''[summary]
            The set of node labels currently defined within the graph.
            Returns:
                [List] -- [Node labels]
        '''
        return self.schema.node_labels

    def get_all_relationship_types(self):
        '''[summary]
            The set of relationship types currently defined within the graph.
            Returns:
                    [List] -- [Relationship types]
        '''
        return self.schema.relationship_types

    def get_sres_by_cypher(self, qry):
        '''[summary]
            Match/Search subgraph by run cypher.
            Arguments:
                qry {[Str]} -- [The query cypher language]
            Returns:
                [List] -- [a List of Dictionaries(start_node, relationship, end_node)]
        '''
        rs = []
        try:
            r_ori = g.run(qry)
            for r in r_ori:
                for _, v in r.items():
                    _type = get_name(v)
                    if _type in ['Node']:
                        rs.append({
                            'type': 'Node',
                            'labels': list(v.labels),
                            'properties': dict(v),
                        })
                    else:
                        rs.append({
                            'type': 'Relationship',
                            'labels': _type,
                            'properties': dict(v),
                        })

        except Exception as Err:
            return Err
        return rs
