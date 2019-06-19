# -*- coding: utf-8 -*-

import os, sqlite3

db_file = os.path.join(os.path.dirname(__file__), 'test.db')
if os.path.isfile(db_file):
	os.remove(db_file)

# 初始数据:
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute('create table user(id varchar(20) primary key, name varchar(20), score int)')
cursor.execute(r"insert into user values ('A-001', 'Adam', 95)")
cursor.execute(r"insert into user values ('A-002', 'Bart', 62)")
cursor.execute(r"insert into user values ('A-003', 'Lisa', 78)")
cursor.close()
conn.commit()
conn.close()
#返回指定分数区间的名字，按分数从低到高排序 
def get_score_in(low, high):
	if low>high:
		print('错误的分数段, high 必须高于 low')
		return
	if low<0:
		print('错误的分数段, low 必须高于 0')
		return
	if high>100:
		print('错误的分数段, high 必须小于 100')
		return
	try:
		L=[]
		conn = sqlite3.connect('test.db')
		cursor = conn.cursor()
		sql="select name from user where score between ? and ? order by score"
		args=[low,high]
		cursor.execute(sql,args)
		values = cursor.fetchall()
		for i in values:
			L.append(i[0])
	finally:
		cursor.close()
		conn.close()
	return L
	
#测试
values=get_score_in(80, 900)
print(values)
assert get_score_in(80, 95) == ['Adam'], get_score_in(80, 95)
assert get_score_in(60, 80) == ['Bart', 'Lisa'], get_score_in(60, 80)
assert get_score_in(60, 100) == ['Bart', 'Lisa', 'Adam'], get_score_in(60, 100)
print('Pass')