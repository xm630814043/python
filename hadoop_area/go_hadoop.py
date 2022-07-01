# -*- coding: UTF-8 -*-
# 获取当前网页内容并获取
import sys
import os
from time import ctime, sleep
import random
reload(sys)
sys.setdefaultencoding('utf-8')

chufa = [      
		'金牛区,金牛,茶店子投递站,火车北站投递,沙湾分局投递,天回镇投递,簸箕街投递站,商函局大宗邮件,包裹业务局营业部,投递局沙湾投递部,土桥投递站,邮政局大宗邮件'
        ]
daoda =[
		'安县,宝林邮政,沸水邮政,河清邮政,黄土邮政,界牌,雎水邮政,乐兴邮政,清泉邮政,桑枣邮政,石鸭,塔水邮政,周礼晓坝邮政,秀水邮政,迎新邮政,永河邮政',
		'安岳局递送分局',
		'巴州区投递中心,巴州区商投',
		'苍溪邮政投递分局',
		'翠屏区,安阜',
		'大英县邮政投递',
		'大竹县邮政收投班',
		'丹棱县投递局',
		'峨眉山市,峨眉山市邮件运输处理,峨山邮政,符溪邮政,桂花桥邮政,九里邮政,乐都邮政,龙池邮政,罗目邮政,双福邮政,投递一部',
		'恩阳区,巴中上八庙,巴中市茶坝,巴中市恩阳,巴中市花丛,巴中市麻石,巴中市雪山,巴中市渔溪,巴中市玉山',
		'富顺县投递',
		'高县邮政局投递',
		'珙县投递',
		'古蔺县邮政投递',
		'广安区,白市,大安,大龙,观阁,观塘,广福邮政,桂兴,恒升邮政,虎城,井河,浓溪,石笋,肖溪,协兴邮政,枣山',
		'广汉市雒城投递,广汉城区营揽投',
		'汉源县邮政投递',
		'合江县邮政投递',
		'洪雅县投递局',
		'夹江县投递',
		'犍为邮政封发投递',
		'简阳市局投递',
		'剑阁邮政投递',
		'江安县,江安发行递送',
		'江阳区,江阳,丹林,江北邮政,蓝田邮政,邻玉,泸州市营,弥陀邮政,茜草邮政,石棚,石寨,通滩邮政,宜定',
		'江油邮政局投递',
		'井研县收投',
		'筠连发行投递',
		'阆中市七里投递,阆中市投递中心',
		'隆昌县邮政投递',
		'泸县邮政投递',
		'罗江县万安投递',
		'绵竹市剑南投递,绵竹城区营揽投',
		'名山邮政投递',
		'南部县投递中心',
		'南江县投递中心',
		'彭山县投递分局',
		'蓬安县投递中心',
		'蓬溪县邮政投递',
		'平昌县投递中心',
		'青川分拣封发投递',
		'渠县邮政局收投班',
		'仁寿县商投,仁寿县邮政投递局',
		'荣县投递',
		'三台县城区投递',
		'射洪县邮政投递',
		'什邡市雍城投递,什邡城区营揽投',
		'通江县投递中心',
		'万源邮政局收投班',
		'旺苍邮政收投分局',
		'威远县邮政投递',
		'西昌市,西昌,航天大道投递,新村',
		'兴文邮政投递',
		'叙永县邮政投递部',
		'宣汉邮政局投递班',
		'盐亭县城区投递',
		'仪陇县投递中心',
		'宜宾县发行投递,宜宾报刊投递',
		'营山县投递中心',
		'游仙揽投',
		'岳池县邮政投递',
		'长宁投递',
		'中江县凯江投递,中江伍城营揽投',
		'资中县邮政投递',
		'梓潼县城区投递'
        ]

if __name__ == "__main__":
    
    countdaoda = len(daoda)
    countchufa = len(chufa)
    commandline = 'hadoop jar /home/hadoop/hadoop-2.7.3/share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar -D stream.map.output.field.separator=\'\t\' -D stream.num.map.output.key.fields=2 -D map.output.key.field.separator=\'\t\' -D num.key.fields.for.partition=2 -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner '
    
    input = '-input /home/hadoop/YZshuju/quxian/jinniu/mappers/ '
    
    print countdaoda,countchufa
    for i in range(countdaoda):
        if countchufa == countdaoda:
            chifa_mudi = chufa[i] + ' ' + daoda[i]
            fajian=chufa[i].split(',')
        elif countchufa == 1:
            chifa_mudi = chufa[0] + ' ' + daoda[i]
            fajian=chufa[0].split(',')
        else:
            print 'chufa != daoda'
            quit()
        
        shoujian=daoda[i].split(',')
        chifa_mudi_name = fajian[0] + ' ' + shoujian[0]
        mapper = '-mapper \'python /home/hadoop/chinapost/mapperc.py ' + chifa_mudi + '\' '
        reducer = '-reducer \'python /home/hadoop/chinapost/reducerc.py ' + chifa_mudi + '\' '
        output = '-output /home/hadoop/YZresult/zhuyaoquxian/jinniu/' + chifa_mudi_name.replace(' ','_')
    
        command = commandline + mapper + reducer + input + output
        #command = commandline + mapper + input + output
        print command
    
        os.system(command)
        sleep(random.randint(60,90))
    
    





