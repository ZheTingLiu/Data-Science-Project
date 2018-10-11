import re
import time
import jieba
import logging
def read_file():
	start = time.time()
	print("start read file")
	f = open('comment.txt','r',encoding = 'utf-8')
	comment = []
	author = []
	for row in f.readlines():
		tmp = "".join(row.split(':')[1:])
		if tmp not in comment:
			if not re.search('http',tmp):
				# print(tmp)
				comment.append(tmp)
				author.append(row.split(':')[0])
	f.close()
	print(time.time()-start)
	print("start write file")
	f = open('train_comment.txt','w',encoding = 'utf-8')
	file = open('train_author.txt','w',encoding = 'utf-8')
	for r,a in zip(comment,author):
		f.write(r+'\n')
		file.write(a+'\n')
	f.close()
	file.close()
	print(time.time()-start)
