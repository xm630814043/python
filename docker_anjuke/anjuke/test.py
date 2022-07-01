# -*- coding:UTF-8 -*-
import json

import requests
import random
import pymysql


# ip_list = ["113.238.142.208:3128", "220.181.111.37:80", "124.70.46.14:3128",
#            "183.213.26.12:3128", "202.108.22.5:80", "112.80.248.73:80",
#            "180.97.34.35:80", "42.194.232.51:8088", "47.92.113.71:80",
#            "106.55.15.244:8889", "59.124.224.205:3128"]
# proxy = {'http':"http://" + random.choice(ip_list)}
# print(proxy)

# ip_list = ["113.238.142.208:3128", "220.181.111.37:80", "124.70.46.14:3128",
#            "183.213.26.12:3128", "202.108.22.5:80", "112.80.248.73:80",
#            "180.97.34.35:80", "42.194.232.51:8088", "47.92.113.71:80",
#            "106.55.15.244:8889", "59.124.224.205:3128"]
# proxy = {"http": "http://" + random.choice(ip_list)}
# print(proxy)
# response = requests.get("https://httpbin.org/get",proxies=proxy, timeout=5)
# print(response)
# print(response.text)

db = pymysql.connect(host="am-bp1y98h053h3267bh167320o.ads.aliyuncs.com", user="sizu", password="uuC4W9YyZ6",database="xpx_tms")
cursor = db.cursor()
if __name__ == '__main__':
    # 打开数据库连接
    fh = open("auto_info.txt", encoding="utf-8")
    for line in fh:
        info = line.replace("\n", "").split("\t")
        sql = "SELECT job_result FROM tms_auto_send_job_result WHERE job_code = %s"  % (info[1])
        print(sql)
        cursor.execute(sql)
        # 获取所有记录列表
        # print(cursor.rowcount)
        results = cursor.fetchone()
        if results:
            for rows in results:
                if rows == "":
                    print(results)
                    fh = open("village_info_file", "a+", encoding="utf-8")
                    fh.write(line)
                    # 文件关闭
                    fh.close()
                else:
                    dicts = json.loads(rows)
                    for dict in dicts:
                        plan_code = ""
                        full_rate = 0.00
                        car_number = ""
                        waybill_ids = []
                        for k, v in dict.items():
                            if k == "plan_code":
                                plan_code = v
                            if k == "full_rate":
                                full_rate = round(v, 2)
                            if k == "car_number":
                                if v == "":
                                    car_number = "派车单关闭"
                                else:
                                    car_number = v
                            if k == "waybill_ids":
                                waybill_ids = v
                        plan_info = line.replace("\n", "") + "\t" + plan_code + "\t" + str(
                            full_rate) + "\t" + car_number + "\t" + str(len(waybill_ids))
                        print(plan_info)
                        fh = open("village_info_file", "a+", encoding="utf-8")
                        fh.write(plan_info + "\n")
                        # 文件关闭
                        fh.close()
        else:
            print(results)
            fh = open("village_info_file", "a+", encoding="utf-8")
            fh.write(line + "\n")
            # 文件关闭
            fh.close()
    db.close()