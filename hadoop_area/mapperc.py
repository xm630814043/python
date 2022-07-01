	# -*- coding: utf-8 -*-
import sys
import re
import time

arraya=[]
arrayb=[]
do=''
dowe = ''
k=0
flag=False
citysum=[]
status = 1 #1--ready 2--start 3--end

fj = sys.argv[1]
arrayq=fj.split(',')

sj = sys.argv[2]
arraysa=sj.split(',')


def delarray(inta):
	if inta == 1:
		del arraya[:]
		del arrayb[:]
		del citysum[:]
	else:
		del arraya[:]
		del arrayb[:]
          
def cityfor():
	flag1=False
	flag3=True
	j=0
	h=0
	#下一站循环
	#print '进入函数,开始遍历筛选'
	i=len(citysum)
	for index in range(len(citysum)):
		j+=1
		cityc=citysum[i-j]
		if flag3:
			for dishicity in arraysa:
				citypipei = dishicity + '[\u4e00-\u9fa5\w\W\d]*'
				pertten1 = re.match(citypipei,cityc)
				if pertten1 != None:
					h+=1
					flag3 = False
					break
			break
	if h > 0 :
		flag1 = True 
		return  flag1
	else:
		return  flag1
                              
for span in sys.stdin:
	if span == do:
		continue
	else:
		do = span 
        
	pertten = re.search('[0-9\d\S\s]*[\u4e00-\u9fa5\w\W\d]*已收寄',span) 
	if pertten != None:
		qianshou = pertten.group().strip()
		worda,counta =qianshou.split('\t',1)
		if worda != dowe:
			delarray(1)
			dowe = worda
			arraya.append(qianshou)
			arrayb.append(qianshou)
			status = 2
			continue
          
	perttens = re.search('[0-9\d\S\s]*[\u4e00-\u9fa5\w\W\d]*正在投递',span) 
	if perttens != None:
		if status == 2:
			paijian = perttens.group().strip()
			wordd,countd =paijian.split('\t',1)
			citydd,cityd = countd.split('\t', 1)
			arraya.append(paijian)
			arrayb.append(paijian)
			citysum.append(cityd)
			continue    
	pertte = re.search('[0-9\d\S\s]*[\u4e00-\u9fa5\w\W\d]*已投到|[0-9\d\S\s]*[\u4e00-\u9fa5\w\W\d]*已妥投|[0-9\d\S\s]*[\u4e00-\u9fa5\w\W\d]*已签收',span)
	if pertte != None:
		if status == 2:          
			qiandao = pertte.group().strip()
			wordb, countb = qiandao.split('\t', 1) 
			arraya.append(qiandao)
			arrayb.append(qiandao)
			#print '调取函数cityfor()=%s'%('判断省份')
			flag=cityfor()
			if flag:
				if len(arrayb) == 3 and worda == wordb:
					k+=1 
					for index in range(len(arraya)):
						print arraya[index]
					status = 1
             
	else:
		if status == 2:
			pertt = re.search('[0-9\d\S\s]*[\u4e00-\u9fa5\w\W\d]*已投到|[0-9\d\S\s]*[\u4e00-\u9fa5\w\W\d]*已妥投|[0-9\d\S\s]*[\u4e00-\u9fa5\w\W\d]*已签收',span) 
			if pertt != None:
				status = 1
				continue
                    
			pert = re.search('[0-9\d\S\s]*[\u4e09fa5\w\W\d]*已收寄',span)
			if pert!= None:
				status = 1
				continue
			if '下一站' in span:
				cit,city = span.split('下一站',1)
				if '中心' in city:
					citya=city.split('中心')
					citysum.append(citya[0])
				else: 
					citysum.append(city.strip())
			arraya.append(span.strip())
#print k

                                                                






