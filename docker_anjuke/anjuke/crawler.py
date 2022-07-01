# -*- coding:UTF-8 -*-
import decimal
import re
import pymysql
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import random

# 打开数据库连接
db = pymysql.connect(host="rm-bp1457tgaf4pd3zn6to.mysql.rds.aliyuncs.com", user="ectouch", password="Vfr456789ol",database="xpx_tms")
cursor = db.cursor()

def db_insert(list):
    fh = open("village_info_file", "a+", encoding="utf-8")
    # 使用cursor()方法获取操作游标
    sql = "INSERT INTO village_info (area,village_name,trade_area,village_address,house_price,village_time,village_tag,property_type,property_price,build_area_count,village_house_count,parke_space_num,volume_rate,green_rate,development_business,property_business,house_assistant_num,house_rent_num,province,city,village_longitude,village_latitude,village_characteristic,question_answer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    print("执行的sql: ", sql)
    # 执行sql语句
    cursor.execute(sql, list)
    # 数据库关闭
    db.commit()
    fh.write(str(list)+ "\n")
    # 文件关闭
    fh.close()

# 获取城市下小区列表
def analysis_info(content):

    url_list = []
    # 获取小区信息--列表
    time.sleep(random.randint(4, 6))
    f = open("village_url_file",  encoding="utf-8")
    for line in f:
        url_list.append(line.replace("\n",""))

    flag = False
    for row in content:
        area = ""
        name = ""
        address = ""
        # 区域，商圈，地址
        village_detail = []
        house_address = row.find_all("span", attrs={'data-v-3cea202b': ''})
        address_content = re.sub('[\t]', "", re.sub(r'<[^>]+>', "", str(house_address[2])))
        village_info = address_content.replace(" ", "").split("-")
        if len(village_info) != 0:
            area = village_info[0]
        if area == "":
            continue
        village_detail.append(area)
        # print("省，市，区",village_detail)
        # 小区名称
        house_name = row.find(class_="nowrap-min li-community-title")
        name_content = re.sub('[\t]', "", re.sub(r'<[^>]+>', "", str(house_name)))
        village_detail.append(name_content)
        if len(village_info) > 1:
            name = village_info[1]
        village_detail.append(name)
        if len(village_info) > 2:
            address = village_info[2]
        village_detail.append(address)
        # print("小区名字，商圈，地址", village_detail)
        # 房价
        price = row.find(class_="community-price")
        price_content = re.sub('[\t\n]', "", re.sub(r'<[^>]+>', "", str(price))).replace(" ", "")
        if price_content == '暂无均价':
            village_detail.append(0)
        else:
            village_price = price_content.split("元")
            village_detail.append(int(village_price[0])*100)
        # print("房价", village_detail)
        # 建成时间
        times = row.find(class_="year")
        times_content = re.sub('[\t]', "", re.sub(r'<[^>]+>', "", str(times)))
        village_time = times_content.split("年")
        village_detail.append(village_time[0])
        # print("建成时间", village_detail)
        # 标签
        tag = row.find_all(class_="prop-tag")
        tag_content = re.sub('[\t]', "", re.sub(r'<[^>]+>', "", str(tag)))
        village_tag = tag_content.replace("[", "").replace("]", "")
        village_detail.append(village_tag)
        # print("标签", village_detail)
        # info = "上海, " + "上海, " + area + name_content + "\t" + "时间：" + times_content+ "\t" + "价格：" + price_content.replace(" ", "") + "\t" + "标签：" + tag_content + "\t"
        print("获取小区详情，url：", row["href"])
        if row["href"] in url_list:
            continue
        else:
            fh = open("village_url_file", "a+", encoding="utf-8")
            fh.write(row["href"] + "\n")
            fh.close()
        village_list = analysis_detail(row["href"])
        if village_list == []:
            flag = True
            break
        village_detail.extend(village_list)
        db_insert(village_detail)
        time.sleep(random.randint(8,10))
    return flag

# 获取小区详情
def analysis_detail(url):

    ip_list = ["http://113.238.142.208:3128","http://220.181.111.37:80/","http://124.70.46.14:3128/","http://183.213.26.12:3128/","http://202.108.22.5:80/","http://112.80.248.73:80/","http://180.97.34.35:80/","http://42.194.232.51:8088/","http://47.92.113.71:80/","http://106.55.15.244:8889/","http://59.124.224.205:3128/"]
    proxies = {"http": "http://" + random.choice(ip_list), }
    r = requests.get(url, headers=get_headers(), proxies=proxies, timeout=5)
    # r = requests.get(url, headers=get_headers())
    # print("获取小区详情",r.text)
    soup = BeautifulSoup(r.text, "html.parser")
    village_detail = ["物业类型","物业费","总建面积","总户数","停车位","容积率","绿化率","开发商","物业公司","二手房","租房"]
    # 获取小区所属省，市
    location = soup.find("meta",attrs={"name":"location"})
    if location == None:
        print("小区位置获取失败：", location)
        return []
    print("小区位置信息：",location)
    village_location = location["content"].split("=")
    if len(village_location) == 0:
        return "小区详情经纬度解析失败"
    if len(village_location) != 0:
        province = village_location[1].split(";")
        village_detail.append(province[0])

        city = village_location[2].split(";")
        village_detail.append(city[0])

    # 获取小区经纬度
    temps = soup.find_all("script")
    # print("获取所有script对象内容",temps[16].get_text())
    if len(temps) > 16:
        pattern = re.findall(r".+?lat :(.*).+lng :(.*?\n)", str(temps[16].get_text()), re.MULTILINE | re.DOTALL)
        # print("百度地图", type(pattern[0]))
        pattern_content = "".join(tuple(pattern[0]))
        longitude = re.sub('["\t\n"]', "", pattern_content).replace(" ", "").split(",")
        # print("小区经纬度", longitude)
        # 经度
        village_detail.append(decimal.Decimal(longitude[1]))
        # 纬度
        village_detail.append(decimal.Decimal(longitude[0]))

    # 获取小区详情
    basic_info = soup.find(class_="basic-infos-box")
    basic = basic_info.find(class_="basic-parms-mod")
    type_list = basic.find_all("dt")
    type_values = basic.find_all("dd")
    comment_infos = ""
    for index in range(len(type_list)):
        type_content = re.sub('[\t\n]', "", re.sub(r'<[^>]+>', "", str(type_list[index]))).replace("  ", "")
        type_value = re.sub('[\t\n]', "", re.sub(r'<[^>]+>', "", str(type_values[index])))
        if type_content == "物业类型：":
            village_detail[0] = type_value
        elif type_content == "物业费：":
            property_price = type_value.split("元")
            if property_price[0] == "暂无数据":
                village_detail[1] = 0
            else:
                village_detail[1] = int(float(property_price[0]) * 100)
        elif type_content == "总建面积：":
            build_area_count = type_value.split("m")
            village_detail[2] = build_area_count[0]
        elif type_content == "总户数：":
            village_house_count = type_value.split("户")
            village_detail[3] = village_house_count[0]
        elif type_content == "停车位：":
            village_detail[4] = type_value
        elif type_content == "容积率：":
            village_detail[5] = type_value
        elif type_content == "绿化率：":
            green_rate = type_value.split("%")
            village_detail[6] = green_rate[0]
        elif type_content == "开发商：":
            village_detail[7] = type_value
        elif type_content == "物业公司：":
            village_detail[8] = type_value
    # 二手房
    house = basic_info.find(class_="houses-sets-mod j-house-num")
    baseinfopro = house.find("a",attrs={"data-soj":"baseinfopro"})
    house_assistant_num = re.sub('[\t\n]', "", re.sub(r'<[^>]+>', "", str(baseinfopro)))
    if house_assistant_num != "":
        house_num = house_assistant_num.split("套")
        village_detail[9] = house_num[0]
    # 租房
    baseinfozu = house.find("a",attrs={"data-soj":"baseinfozu"})
    house_rent_num = re.sub('[\t\n]', "", re.sub(r'<[^>]+>', "", str(baseinfozu)))
    if house_rent_num != "":
        house_count = house_rent_num.split("套")
        village_detail[10] = house_count[0]

    # 获取小区特色--详情
    comment_list = soup.find_all(class_="multi-dd")
    for row in comment_list:
        info = row.find_all("p")
        comment_info = re.sub('[\t]', "",re.sub(r'<[^>]+>', "", str(info)))
        comment_infos = comment_infos + comment_info
    # print("特色：", comment_infos)
    village_detail.append(comment_infos.replace("[", "").replace("]", ""))

    # 获取小区问答--详情
    question_answer = soup.find(class_="cm-qa-mod")
    question_answer_content = re.sub('[\t\n]', "", re.sub(r'<[^>]+>', "", str(question_answer)).replace(" ", ""))
    # print("问答：", question_answer_content)
    village_detail.append(question_answer_content)
    return village_detail


# 请求抬头
def get_headers():
    # ua = UserAgent(use_cache_server=False)
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36']
    headers = {
        "accept" :"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        "cookie" :"aQQ_ajkguid=09630987-7675-D5E5-B60F-BCFF3AC3BDD4; id58=CpQBZWG78vS97S/sYkw/Ag==; cmctid=483; sessid=5909F4A8-C809-0E6B-A6BA-761E56425FF0; twe=2; ctid=12; wmda_uuid=106120c0923df5f1b9937b8d17f390e9; wmda_new_uuid=1; wmda_visited_projects=%3B6289197098934; fzq_h=a7d6b7d849997e6721f45241037977b6_1639963022273_b67dcb7b0545464cac37c8201631270c_3752220348; ajk-appVersion=; wmda_session_id_6289197098934=1639971621097-8497428b-0ff9-40f4; fzq_js_anjuke_xiaoqu_pc=edec2f0818dcdc3e70cd553c2cb32db2_1639971621962_25; obtain_by=2; xxzl_cid=cbe556f8da734004821fb648180a137f; xzuid=63bb07d0-9118-4f5a-bfb5-08cf6be995bd",
        "referer": "https://guangzhou.anjuke.com/community/view/464907",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": random.choice(user_agent_list)
    }
    return headers


def get_link(url):
    ip_list = ["http://113.238.142.208:3128","http://220.181.111.37:80/","http://124.70.46.14:3128/","http://183.213.26.12:3128/","http://202.108.22.5:80/","http://112.80.248.73:80/","http://180.97.34.35:80/","http://42.194.232.51:8088/","http://47.92.113.71:80/","http://106.55.15.244:8889/","http://59.124.224.205:3128/"]
    proxies = {"http": "http://" + random.choice(ip_list), }
    r = requests.get(url, headers=get_headers(), proxies=proxies, timeout=5)
    # print("城市信息",r.text)
    soup = BeautifulSoup(r.text,"html.parser")
    row_list = soup.find_all(class_="li-row")
    if len(row_list) == 0:
        soup = BeautifulSoup(r.content, "html.parser")
        row_list = soup.find_all(class_="li-row")
    print("row_list,城市信息不为空")
    flag = analysis_info(row_list)
    print("小区信息结果：", flag)
    return flag

if __name__ == '__main__':
    for page in range(1,10):
        url = 'https://shanghai.anjuke.com/community/pudong/m256-p'+str(page)+"/"
        flag = get_link(url)
        print("最终结果取值：", flag)
        print("已完成当前第", str(page), "页数据获取")
        if flag:
            break

    # analysis_info()
    # village_detail = analysis_detail()
    # print(village_detail)
    db.close()
    # analysis_city()
    # db_client()
    # 时间，价格，物业费，总户数，停车位，总建面积，绿化率，二手房源，租房数，全部转为整数
    # 容积率 dcimenal，保留两位，
    # 省市区，单独存储
    # 标签，以逗号分割，存储字符串。
    # 地址分开
