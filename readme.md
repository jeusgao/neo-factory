# NeoFactory

## init_load_csv(fpath, label, index)
## build_cypher
## NeoCreator:
    add_node(label, **properties)
    add_relationship(node_subj, r_type, node_obj)
    create_index(label, keys):

## NeoModifier:
    update_node(node, labels=None, **properties)
    rm_node(node)
    rm_node_label(node, labels)
    rm_node_all_labels(node)
    update_relationship_properties(r, **properties)
    separate_relationship(r)
    drop_index(label, keys)

## NeoSeeker(TransBase):
    get_nodes()
    get_relationhships()
    get_indexes(label)
    get_all_node_labels()
    get_all_relationship_types()
    search()


### Add a relationship
	MATCH (n:User {USER_LOGIN_NAME:'dengxiaoning'})-[r]-(p) RETURN n,r,p
	MATCH (n:User) where n.USER_POST=~'副总裁.*' RETURN n
	MATCH (u:User),(d:Dept) WHERE u.DEPT_CODE = d.DEPT_CODE CREATE (u)-[:MEMBER_OF]->(d)

### Modify a relationship
	[separate(delete) relationship from subgraph first, then re-add a new relationship.]
	g.separate(relation)
	_q = "MATCH (u:User),(d:Dept) WHERE u.USER_LOGIN_NAME = 'dengxiaoning' AND d.DEPT_CODE='LR040201' CREATE (u)-[:Leaderof {ref:'兼任总经理'}]->(d)"
	g.run(_q)

### Create a index
	CREATE INDEX ON :Dept(DEPT_CODE)

### Import from csv
	_query = [
	    "CREATE (c:Company {CMPY_NAME:'联仁健康', CMPY_CODE:'ruaho'})",
	    'LOAD CSV WITH HEADERS FROM "file:/lr/USER.csv" AS row CREATE (n:User) SET n = row',
	    'LOAD CSV WITH HEADERS FROM "file:/lr/DEPT.csv" AS row CREATE (n:Dept) SET n = row',
	    'CREATE INDEX ON :User(USER_LOGIN_NAME)',
	    'CREATE INDEX ON :Dept(DEPT_CODE)',
	    'MATCH (u:User),(d:Dept) WHERE u.DEPT_CODE = d.DEPT_CODE CREATE (u)-[:MEMBER_OF]->(d)',
	    'MATCH (d:Dept),(c:Company) WHERE d.DEPT_PCODE = c.CMPY_CODE CREATE (d)-[:SUB_OF]->(c)',
	    'MATCH (d:Dept),(d1:Dept) WHERE d.DEPT_PCODE = d1.DEPT_CODE CREATE (d)-[:SUB_OF]->(d1)',
	]
	for _q in _query:
	    g.run(_q)

# 模板：
## example(sample.csv):
a_label|a_properties|b_label|r_type|r_properties|conditions|output
-|:-|:-|:-|:-|:-|-:
a:User|{key:'value'}|b:Dept|r:IN_CHARGE_OF|{ref:'兼任总经理'}|a.key=value and b.key=value|output参考模板说明

# 模板说明：
## conditions: 
***value 一定要用单引号引起来***
*例如：a.USER_LOGIN_NAME='gaojinsong00' and b.DEPT_CODE='LR021201'*

## output: 
### Search: 
***直接输入要return的元素(a,b,r之一或多)***
```
a,r,b
```

### Node update
#### Node(s):
##### 创建Node: 
***创建Node时只需要填写a_label和a_properties，a_properties样例: {a:'b', c:'d'}***
```
CREAT_NODE
```

##### 删除Node(s)：
***Node的删除定义为每次只能删除一个label的节点(s)，保险起见请务必认真检查where条件***
```
@DELETE a

*慎用！删除Node(s)前需要先删除与Nodes连接的所有关系*
*如需要批量删除时请使用graph_factory*
```

#### Labels:
##### 新增Node的label(s)：
```
@SET a:label1:label2
```

##### 删除Node的label(s):
```
@REMOVE a:label1:label2
```

### Properties:
##### 新增/修改/删除Node的某些属性：
***设置属性值为 null 即为删除该属性(V4.x以上支持)***
```
@SET a.属性名=属性值, a.属性名2=属性值2, a.属性名3=null
```

##### 删除Node某个属性：
```
@REMOVE a.属性名
```

##### 删除多个属性：
```
@SET a.属性名=null, a.属性名2=null, a.属性名3=null
```

### Relationship update:
##### Create: 
***创建关系时 a, b 两个Node都需要定义，可以是相同label，根据where条件设置可以创建多对Nodes的关系***
```
CREATE_RELATIONSHIP
```

##### 删除关系(s)：
```
@DELETE r
```

##### 修改关系：
***r_type不为空时将修改关系原为r_type的关系，否则修改所有满足 a,b conditions的Nodes对的关系***
```
@CREATE (a)-[r2:NEW_RELATIONSHIP]->(b) SET r2=r WITH r DELETE r
```

##### 修改关系属性：
```
@SET r={TEST:'dddd'}	*替换原有属性*
@SET r.new_property='new_property'	*新增属性*
```

##### 删除关系属性：
```
@REMOVE r.property1, r.property2
```
