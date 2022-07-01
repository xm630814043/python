# -*- coding: utf-8 -*-
import re
import sys
import time

#存储地域走向
arrayx = []
#存储地域走向数量

arrayy = []
#总节点数
x=0
#总单数
y=0
#去除相邻重复
do = ''
#有效单数
k = 0
#置位
status = 1
#地域走向缓存
arrayc=[]
#路线时间处理缓存
arrayb=[0,0,0,0]
#网运时间缓存
arrayd=[]
arraya=[]
#路线时间初始化
lanshousum = 0
wangyunsum = 0
toudisum = 0
zongjisum = 0
#接收网运文本
line = ''

fj = sys.argv[1]
arrayq=fj.split(',')

sj = sys.argv[2]
arrayw=sj.split(',')

def delarray(inta):
	if inta == 1:
		del arrayc[:]
		del arrayd[:] 
        
def timechuli():     
	#地域走向初始化
	str = arrayq[0]
	flagst = True
	citya = ''
	for math in arrayb:
		if math == 0: 
			del arrayc[:]
			flagst = False
			return 1,1,1
			break
     
	if flagst:
		for city in arrayc:
			if city == citya:
				continue
			citya = city
			str = str + '|' + city
		str = str + '|' + arrayw[0]
		if str not in arrayx:
			arrayx.append(str)
			arrayy.append(1)
		else:
			for indes in range(len(arrayx)): 
				if arrayx[indes] == str:
					arrayy[indes]=arrayy[indes]+1
					break
                              
		lanshoutime = arrayb[1] - arrayb[0]
		wangyuntime= arrayb[2] - arrayb[1]
		touditime = arrayb[3] - arrayb[2]  
		#print  lanshoutime,wangyuntime,touditime    
		return lanshoutime,wangyuntime,touditime

for span in sys.stdin:
	if span == do:
		continue
	else:
		do = span
	pertten = re.search('[0-9\d\S\s]*[\u4e00-\u9fa5\w\W\d]*已收寄',span)
	if pertten != None:
		delarray(1)
		for indexs in range(len(arrayb)):
			if arrayb[indexs] != 0:
				arrayb[indexs] = 0  
		shoujian = pertten.group().strip()
		word,count =shoujian.split('\t',1)
		stimes = count[:10] +' '+ '19:00:00'
		bijiaotime = time.mktime(time.strptime(stimes, '%Y-%m-%d %H:%M:%S'))
		stime = count[:20].strip()
		shoujiantime = time.mktime(time.strptime(stime, '%Y-%m-%d %H:%M:%S'))
		arrayb[0] = shoujiantime
		if shoujiantime < bijiaotime:
			status = 2
		else:
			status = 1
		continue  
	pertt = re.search('[0-9\d\S\s]*[\u4e00-\u9fa5\w\W\d]*正在投递',span)
	if pertt != None:
		if status == 2:
			if len(arrayd) != 0:
				arrayb[1] = arrayd[0]
			paijian = pertt.group().strip() 
			wordc,countc =paijian.split('\t',1)
			stimec = countc[:20].strip()
			paijiantime = time.mktime(time.strptime(stimec, '%Y-%m-%d %H:%M:%S'))                                                                                                                                               
			arrayb[2] = paijiantime
			continue   
	pert = re.search('[0-9\d\S\s]*[\u4e00-\u9fa5\w\W\d]*已投到|[0-9\d\S\s]*[\u4e00-\u9fa5\w\W\d]*已妥投|[0-9\d\S\s]*[\u4e00-\u9fa5\w\W\d]*已签收',span)
	if pert != None:
		if status == 2:            
			qianshou = pert.group().strip()
			wordd,countd =qianshou.split('\t',1)
			stimed = countd[:20].strip()
			qianshoutime = time.mktime(time.strptime(stimed, '%Y-%m-%d %H:%M:%S'))  
			arrayb[3]=qianshoutime
			if word == wordd:
				lanshou,wangyun,toudi = timechuli()
				if wangyun !=1 and toudi !=1:
					arraya.append(wordd)
					#print lanshou,wangyun,toudi
					k +=1
					lanshousum = lanshousum + lanshou
					wangyunsum = wangyunsum + wangyun
					toudisum  = toudisum + toudi
					status = 1
                                                              
	else:
		if status == 2:
			line = span.strip()
			wordb,countb = line.split('\t',1)
			if '下一站' in countb:
				cit,city = countb.split('下一站',1)
				if '中心' in city:
					citya=city.split('中心')
					arrayc.append(citya[0])
				else: 
					arrayc.append(city.strip())
			stimeb = countb[:20].strip()
			daodatime = time.mktime(time.strptime(stimeb, '%Y-%m-%d %H:%M:%S'))
			arrayd.append(daodatime)
			continue

if k != 0:
	zongjisum = lanshousum + wangyunsum + toudisum
	print k
	zongjiAVG= zongjisum/k               
	lanshouAVG =lanshousum/k
	wangyunAVG =wangyunsum/k
	toudiAVG =toudisum/k
    
	zongjiH= float(zongjiAVG / 3600)
	lanshouH = float(lanshouAVG / 3600)
	wangyunH = float(wangyunAVG / 3600)
	toudiH = float(toudiAVG / 3600)
    
	print "%.2f" % (zongjiH) 
	print "%.2f" % (lanshouH) 
	print "%.2f" % (wangyunH) 
	print "%.2f" % (toudiH)
else:
   print '揽收,网运,投递为0'

if len(arrayx) !=0:
	for lis in range(len(arrayx)):
		print arrayx[lis]+'\t'+str(arrayy[lis])
          
if len(arrayx):
	for  danhao in arraya:
			print danhao
print 'reduce end!'

     

