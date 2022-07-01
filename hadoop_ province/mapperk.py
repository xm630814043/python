# -*- coding: utf-8 -*-
import sys
import re
import time
		   
timea=0
timeb=0
timec=0
timed=0
do=''
dowe = ''
k = 0
arraya=[]
citysum=[]
citysum1=[]
status = 1 #1--ready 2--start 3--end

#*前提是中山市，中山属于大众词语，重复值多，需要在目的地arrayw，array_city中去掉
#bidui数组中如果添加'中山板芙','中山北投','中山大涌','中山东二','中山东凤','中山东升','中山东投','中山东一','中山阜沙','中山港口','中山古镇','中山横栏','中山黄圃','中山六投','中山民众','中山南朗','中山南区','中山南头','中山三角','中山三乡','中山沙溪','中山神湾','中山坦洲','中山西投','中山小榄',
#也必须在array_city中添加        
#bidui=['白云','城关','城区','城中','鼓楼','海州','和平','河东','江北','矿区','龙华','南山','普陀','桥东','桥西','市中','铁东','铁西','通州','青山','西湖','新华','永定','长安','朝阳']

fj = sys.argv[1]
arrayq=fj.split(',')

sj = sys.argv[2]
array1=sj.split(',')

def delarray(inta):
    if inta == 1:
		del arraya[:]
		del citysum[:]
		del citysum1[:]
 
 
def cityfor():
	flag1=False
	flag2=False
	flag3=True
	flag4=False
	flag5=True
	j=0
	f=0
	h=0
	chinacitys=''
	#下一站、正在投递
	#print '进入函数,开始遍历筛选'
	i=len(citysum)
	i1=len(citysum1)
	#循环遍历缓存下一站,正在投递数据
	for index in range(len(citysum)):
		j+=1
		#输出缓存最后一个值'daipipei'匹配是否是所要地市
		daipipei=citysum[i-j]
		cityshaixuan = array1[0] + '[\u4e00-\u9fa5\w\W\d]*'
		pertten1 = re.match(cityshaixuan,daipipei)
		if pertten1 != None:
			flag2 = True
			break 
	#目的地 
	if flag2:
		for index1 in range(len(citysum)):
			daipipei1=citysum[i-j]
			#判断输出在地市下标如果没匹配成功，则不是所要单号
			if index1 > j:
				flag3 = False
			if flag3:	
				for citys in array1:
					cityshaixuan1 = citys + '[\u4e00-\u9fa5\w\W\d]*'
					pertten2 = re.match(cityshaixuan1,daipipei1)
					if pertten2 != None:
						flag4 = True 
						flag3 = False
						break
			    #break
	#下一站
	if flag4:
		for index2 in citysum1:   
			f+=1
			cityc2=citysum1[i1-f]
			#如果是正在匹配成功，判断其是否是偶然，再次在下一站中判断
			if flag5:
				for citys1 in array1:
					cityshaixuan2 = citys1 + '[\u4e00-\u9fa5\w\W\d]*'
					pertten3 = re.match(cityshaixuan2,cityc2)
					if pertten3 != None: 
						h+=1
						flag5 = False
						break
				break

	if h > 0:
		flag1 = True 
		return flag1 
	else:
		return flag1 
        
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
			status = 2
			continue
          
	perttens = re.search('[0-9\d\S\s]*[\u4e00-\u9fa5\w\W\d]*正在投递',span) 
	if perttens != None:
		if status == 2:
			paijian = perttens.group().strip()
			wordd,countd =paijian.split('\t', 1) 
			citydd,cityd = countd.split('\t', 1)
			arraya.append(paijian)
			citysum.append(cityd)
			continue  
                   
	pertte = re.search('[0-9\d\S\s]*[\u4e00-\u9fa5\w\W\d]*已投到|[0-9\d\S\s]*[\u4e00-\u9fa5\w\W\d]*已妥投|[0-9\d\S\s]*[\u4e00-\u9fa5\w\W\d]*已签收',span)
	if pertte != None:
		if status == 2:          
			qiandao = pertte.group().strip()
			wordb, countb = qiandao.split('\t', 1) 
			arraya.append(qiandao)
			#print '调取函数cityfor()=%s'%('判断省份')
			flag=cityfor()
			if flag:
				if worda == wordb: 
					#k+=1 
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
					citysum1.append(citya[0])
				else: 
					citysum.append(city.strip())
					citysum1.append(city.strip())
			arraya.append(span.strip())
			continue
                                                                
#print k







