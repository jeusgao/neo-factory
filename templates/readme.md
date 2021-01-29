#模板：
##example(sample.csv):
a_label|a_properties|b_label|r_type|r_properties|conditions|output
-|:-|:-|:-|:-|:-|-:
a:User|{key:'value'}|b:Dept|r:IN_CHARGE_OF|{ref:'兼任总经理'}|a.key=value and b.key=value|output参考readme.md

#模板说明：
## conditions:
***value 一定要用单引号引起来***
*例如：a.USER_LOGIN_NAME='Samzhang' and b.DEPT_CODE='00001'*

## output:
###Search:
***直接输入要return的元素(a,b,r之一或多)***
```
a,r,b
```

###Node update
####Node(s):
#####创建Node:
***创建Node时只需要填写a_label和a_properties，a_properties样例: {a:'b', c:'d'}***
```
CREAT_NODE
```

#####删除Node(s)：
***Node的删除定义为每次只能删除一个label的节点(s)，保险起见请务必认真检查where条件***
```
@DELETE a

*慎用！删除Node(s)前需要先删除与Nodes连接的所有关系*
*如需要批量删除时请使用graph_factory*
```

####Labels:
#####新增Node的label(s)：
```
@SET a:label1:label2
```

#####删除Node的label(s):
```
@REMOVE a:label1:label2
```

###Properties:
#####新增/修改/删除Node的某些属性：
***设置属性值为 null 即为删除该属性(neo4j V4.x以上支持)***
```
@SET a.属性名=属性值, a.属性名2=属性值2, a.属性名3=null
```

#####删除Node某个属性：
```
@REMOVE a.属性名
```

#####删除多个属性：
```
@SET a.属性名=null, a.属性名2=null, a.属性名3=null
```

### Relationship update:
#####Create:
***创建关系时 a, b 两个Node都需要定义，可以是相同label，根据where条件设置可以创建多对Nodes的关系***
```
CREATE_RELATIONSHIP
```

#####删除关系(s)：
```
@DELETE r
```

#####修改关系：
***r_type不为空时将修改关系原为r_type的关系，否则修改所有满足 a,b conditions的Nodes对的关系***
```
@CREATE (a)-[r2:NEW_RELATIONSHIP]->(b) SET r2=r WITH r DELETE r
```

#####修改关系属性：
```
@SET r={TEST:'dddd'}	*替换原有属性*
@SET r.new_property='new_property'	*新增属性*
```

#####删除关系属性：
```
@REMOVE r.property1, r.property2
```
