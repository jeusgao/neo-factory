#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-30 20:59:38
# @Author  : Joe Gao (jeusgao@163.com)
# @Link    : https://www.jianshu.com/u/3b77f85cc918
# @Version : $Id$

import collections
from models.neo_factory import NeoSeeker

Fields = collections.namedtuple('Fields', ['Node_labels', 'R_types', 'Outputs'])

neo_seeker = NeoSeeker()

node_labels = list(neo_seeker.get_all_node_labels())
r_types = list(neo_seeker.get_all_relationship_types())
outputs = {
    'CREATE_NODE': '*创建Node时只需要填写start_node和a_properties*' +
    '\n\n\t' +
    'a_properties样例: {a:"b", c:"d"}',
    'CREATE_RELATIONSHIP': '*创建关系时 a, b 两个Node都需要定义，可以是相同label，根据where条件设置可以创建多对Nodes的关系*',
    '@SET': '*新增/修改/删除Node的某些属性(设置属性值为 null 即为删除该属性)*' +
    '\n\n\t' +
    '(@SET) a.属性名=属性值,a.属性名2=属性值2,a.属性名3=null' +
    '\n\n' +
    '**修改关系属性**' +
    '\n\n  ' +
    '*替换原有属性*' +
    '\n\n\t' +
    '(@SET) r={TEST:"dddd"}' +
    '\n\n  ' +
    '*新增属性*' +
    '\n\n\t' +
    '(@SET) r.new_property="new_property"',
    '@DELETE': '*Node的删除定义为每次只能删除一个label的节点(s)，保险起见请务必认真检查where条件*' +
    '\n\n  ' +
    '*删除节点*' +
    '\n\n\t' +
    '(@DELETE) a' +
    '\n\n  ' +
    '*删除关系*' +
    '\n\n\t' +
    '(@DELETE) r',
    '@REMOVE': '**删除元素属性**' +
    '\n\n  ' +
    '*删除Node的label*' +
    '\n\n\t' +
    '(@REMOVE) a:label1:label2' +
    '\n\n  ' +
    '*删除Node某个属性*' +
    '\n\n\t' +
    '(@REMOVE) a.属性名' +
    '\n\n  ' +
    '*删除关系的多个属性*' +
    '\n\n\t' +
    '(@REMOVE) r.property1, r.property2',
    '@CREATE': '*r_type不为空时将修改关系原为r_type的关系，否则修改所有满足 a,b conditions的Nodes对的关系*' +
    '\n\n\t' +
    '(@CREATE) (a)-[r2:NEW_RELATIONSHIP]->(b) SET r2=r WITH r DELETE r',
}

NEO_FIELDS = Fields(node_labels, r_types, outputs)
