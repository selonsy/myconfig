# -*- coding:utf-8 -*-
'''
作者：selonsy  时间：2019年6月1日20:05:58
环境：python(3.6.6);mongodb(4.0)
说明：
此页面是python环境下的mongodb使用教程，仅供熟悉基础语法所用。
生产开发建议将常用的操作进行封装，具体可以网上搜索合适的封装类。

目录:
1、数据库连接
2、插入数据
3、查询数据
4、更新数据
5、删除数据
6、条件操作符
7、排序
8、数据处理（过滤）
9、多级路径元素
'''
# 导入包
from pymongo import MongoClient

#########################################################
# 数据库连接
#########################################################
conn = MongoClient('127.0.0.1', 27017)
db = conn.vmatrix       #连接vmatrix数据库，没有则自动创建
my_set = db.test_set    #使用test_set集合，没有则自动创建

#########################################################
# 插入数据
# insert:插入一个列表多条数据不用遍历，效率高
# save:需要遍历列表，一个个插入
# 返回值：数据的id（由mongo生成，如：ObjectId('5cf2666a721cc152e0c37a7c')）
#########################################################
# 插入单条
my_set.insert({"name":"zhangsan1","age":18})
my_set.save({"name":"zhangsan2","age":18})
# 插入多条
users1=[{"name":"zhangsan3","age":18},{"name":"zhangsan4","age":18}]  # 添加多条数据到集合中
users2=[{"name":"zhangsan5","age":18},{"name":"zhangsan6","age":18}]
my_set.insert(users1) 
# my_set.save(users2) # 错误，TypeError: to_save must be an instance of dict, bson.son.SON, bson.raw_bson.RawBSONDocument, or a type that inherits from collections.MutableMapping

#########################################################
# 查询数据
# 注：
# 查询不到则返回None
# save:需要遍历列表，一个个插入
#########################################################
# 查询全部
for i in my_set.find():
    print(i)
# 查询符合条件的集合，如 name=zhangsan 的
for i in my_set.find({"name":"zhangsan1"}):
    print(i)
# 查询符合条件的单个（默认排序方式：ObjectId，升序）
print(my_set.find_one({"name":"zhangsan1"}))

#########################################################
# 更新数据
# 语法：
# my_set.update(
#    <query>,     # 查询条件
#    <update>,    # update的对象和一些更新的操作符
#    {
#      upsert: <boolean>,       # 如果不存在update的记录，是否插入。
#      multi: <boolean>,        # 可选，mongodb 默认是false,只更新找到的第一条记录。
#      writeConcern: <document> # 可选，抛出异常的级别。
#    }
# )
#########################################################
my_set.update({"name":"zhangsan1"},{'$set':{"age":20}})

#########################################################
# 删除数据
# 语法：
# my_set.remove(
#    <query>,                   #（可选）删除的文档的条件。
#    {
#      justOne: <boolean>,      #（可选）如果设为 true 或 1，则只删除一个文档。
#      writeConcern: <document> #（可选）抛出异常的级别。
#    }
# )
#########################################################
# 删除 name=zhangsan 的全部记录
my_set.remove({'name': 'zhangsan6'})

# 删除某个 id 的记录
id = my_set.find_one({"name":"zhangsan5"})["_id"]
my_set.remove(id)

#删除集合里的所有记录
my_set.remove()

#########################################################
# 条件操作符：
#    (>)    大于        -  $gt
#    (<)    小于        -  $lt
#    (>=)   大于等于    -  $gte
#    (<= )  小于等于    -  $lte
# 
# 类型判断：
# Double                1     
# String                2     
# Object                3     
# Array                 4     
# Binary data           5     
# Undefined             6    已废弃
# Object id             7     
# Boolean               8     
# Date                  9     
# Null                  10     
# Regular Expression    11     
# JavaScript            13     
# Symbol                14     
# JavaScript (with scope)    15     
# 32-bit integer        16     
# Timestamp             17     
# 64-bit integer        18     
# Min key               255    Query with -1.
# Max key               127  
#########################################################
# 查询集合中age大于25的所有记录
for i in my_set.find({"age":{"$gt":25}}):
    print(i)
# 找出name的类型是String的
for i in my_set.find({'name':{'$type':2}}):
    print(i)
    
#########################################################
# 排序
# 
# 在MongoDB中使用sort()方法对数据进行排序。
# sort()方法可以通过参数指定排序的字段，并使用 1 和 -1 来指定排序的方式，其中 1 为升序，-1 为降序。
#########################################################
# 将查询的结果按照 age 升序进行排序
for i in my_set.find().sort([("age",1)]):
    print(i)
    
#########################################################
# 数据处理
# limit()：方法用来读取指定数量的数据
# skip()： 方法用来跳过指定数量的数据
# IN：表示查询范围
# OR：或
# all：查看是否包含全部条件
# push：填充数据
# pushAll：填充多个数据
# pop：移除最后一个数据
# pull：按值移除数据
# pullAll：移除多个数据
#########################################################
# 下面表示跳过两条数据后读取6条
for i in my_set.find().skip(2).limit(6):
    print(i)
# 找出 age 是20、30、35的数据
for i in my_set.find({"age":{"$in":(20,30,35)}}):
    print(i)
# 找出 age 是20或35的记录
for i in my_set.find({"$or":[{"age":20},{"age":35}]}):
    print(i)
'''
dic = {"name":"lisi","age":18,"li":[1,2,3]}
dic2 = {"name":"zhangsan","age":18,"li":[1,2,3,4,5,6]}

my_set.insert(dic)
my_set.insert(dic2)
'''
# 查看包含 1,2,3,4 的数据（即刚插入的dic2），输出为：{'_id': ObjectId('58c503b94fc9d44624f7b108'), 'name': 'zhangsan', 'age': 18, 'li': [1, 2, 3, 4, 5, 6]}
for i in my_set.find({'li':{'$all':[1,2,3,4]}}):
    print(i)
# 往 name=lisi 的数据里的 li 字段中填充 4
my_set.update({'name':"lisi"}, {'$push':{'li':4}})
for i in my_set.find({'name':"lisi"}):
    print(i) # 输出：{'li': [1, 2, 3, 4], '_id': ObjectId('58c50d784fc9d44ad8f2e803'), 'age': 18, 'name': 'lisi'}
my_set.update({'name':"lisi"}, {'$pushAll':{'li':[4,5]}})
for i in my_set.find({'name':"lisi"}):
    print(i) # 输出：{'li': [1, 2, 3, 4, 4, 5], 'name': 'lisi', 'age': 18, '_id': ObjectId('58c50d784fc9d44ad8f2e803')}
# 移除 name=lisi 的数据里的 li 字段的最后一个元素(-1为移除第一个)
my_set.update({'name':"lisi"}, {'$pop':{'li':1}})
for i in my_set.find({'name':"lisi"}):
    print(i) # 输出：{'_id': ObjectId('58c50d784fc9d44ad8f2e803'), 'age': 18, 'name': 'lisi', 'li': [1, 2, 3, 4, 4]}
# 移除 name=lisi 的数据里的 li 字段中值为 3 的元素，按值移除
my_set.update({'name':"lisi"}, {'$pop':{'li':3}})
my_set.update({'name':"lisi"}, {'$pullAll':{'li':[1,2]}})
for i in my_set.find({'name':"lisi"}):
    print(i) # 输出：{'name': 'lisi', '_id': ObjectId('58c50d784fc9d44ad8f2e803'), 'li': [4, 4], 'age': 18}
    
#########################################################
# 多级路径元素操作
#########################################################
# 先插入一条数据
dic = {"name":"zhangsan",
       "age":18,
       "contact" : {
           "email" : "1234567@qq.com",
           "iphone" : "11223344"}
       }
my_set.insert(dic)

#多级目录用. 连接
for i in my_set.find({"contact.iphone":"11223344"}):
    print(i) # 输出：{'name': 'zhangsan', '_id': ObjectId('58c4f99c4fc9d42e0022c3b6'), 'age': 18, 'contact': {'email': '1234567@qq.com', 'iphone': '11223344'}}

result = my_set.find_one({"contact.iphone":"11223344"})
print(result["contact"]["email"]) # 输出：1234567@qq.com

#多级路径下修改操作
result = my_set.update({"contact.iphone":"11223344"},{"$set":{"contact.email":"9999999@qq.com"}})
result1 = my_set.find_one({"contact.iphone":"11223344"})
print(result1["contact"]["email"]) # 输出：9999999@qq.com

# 对数组用索引操作
dic = {"name":"lisi",
       "age":18,
       "contact" : [
           {
           "email" : "111111@qq.com",
           "iphone" : "111"},
           {
           "email" : "222222@qq.com",
           "iphone" : "222"}
       ]}
my_set.insert(dic)
# 查询
result1 = my_set.find_one({"contact.1.iphone":"222"})
print(result1) # 输出：{'age': 18, '_id': ObjectId('58c4ff574fc9d43844423db2'), 'name': 'lisi', 'contact': [{'iphone': '111', 'email': '111111@qq.com'}, {'iphone': '222', 'email': '222222@qq.com'}]}

# 修改
result = my_set.update({"contact.1.iphone":"222"},{"$set":{"contact.1.email":"333333@qq.com"}})
print(result1["contact"][1]["email"])
#输出：333333@qq.com
