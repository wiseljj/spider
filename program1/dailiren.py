# -*- coding: utf-8 -*-
import requests
import time
import json
from fake_useragent import UserAgent
import random
import copy
from lxml import etree
import re
from pymysql import *
conn = connect(host='127.0.0.1', port=3306, database='spider', user='root', password='mysql',charset='utf8')
# 获得Cursor对象
cs1 = conn.cursor()

# contentId=32885
# 定义空集合l存放useruuid
l = set()
#将某个资讯的所有评论存到一个字典k里面
# k={"code":200,"data":{"commentList":[],"isFinal":True},"info":"操做成功","success":True}
for d in range(100,40000):
    contentId=d
    # 目标url
    url = "https://content.winbaoxian.com/learning/queryLearningCommentList?timestamp=&contentId={}&contentType=0&topCommentId=".format(contentId)
    ua=UserAgent()
    headers = {
        "User-Agent": ua.random
    }
    # print(headers)
    try:
        response = requests.get(url, headers=headers, verify=False)
        print(url)
        print(json.loads(response.text))
        global k
        k=json.loads(response.text).get("data").get("commentList")
        # for a in json.loads(response.text).get("data").get("commentList"):
        #     k.get("data").get("commentList").append(a)
        for b in json.loads(response.text).get("data").get("commentList"):
            p = copy.deepcopy(l)
            l.add(b.get("userUuid"))
            url1 = 'https://app.winbaoxian.com/card/shared/{}?nw=1'.format(b.get("userUuid"))
            # url1 = 'https://app.winbaoxian.com/card/shared/7bd3a19df63e42e99b1cfb450186e511?nw=1'
            response1 = requests.get(url1, headers=headers, verify=False)
            # print(response1.text)
            data = response1.content.decode('utf8')
            html_data = etree.HTML(data)
            name = html_data.xpath("//section/div[1]/div/h2/text()")
            verify = html_data.xpath("//section/div[2]/div/ul/li[1]/div/span[2]/text()")
            company_add = html_data.xpath("//section/div[2]/div/ul/li[2]/div//text()")
            print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW1111111111111111111111")
            if re.search(r'：(.*)', "".join(company_add).strip()):
                q = re.search(r'：(.*)', "".join(company_add).strip()).group(1)
                print("".join(name).strip(), "".join(verify).strip(), q)

            url2 = 'https://ism.winbaoxian.com/insurance/product/100853/detail?u={}'.format(b.get("userUuid"))
            response2 = requests.get(url2, headers=headers, verify=False)
            s = json.loads(response2.text).get("data").get("mobile")
            # print(json.loads(response2.text).get("data").get("mobile"))
            print(s)

            if len(l) != len(p):
                try:
                    sql = "insert into dailiren_copy(userUuid,nickname,company,contentId,name1,verify,company_add,mobile) values('%s','%s','%s',%d,'%s','%s','%s','%s')" % (
                    b.get("userUuid"), b.get("cname"), b.get("company"), contentId, "".join(name).strip(),
                    "".join(verify).strip(), q, s)
                    # sql = "insert into dailiren(userUuid,cname,company,contentId) values('%s','%s','%s',%d)" % (b.get("userUuid"),b.get("cname"),b.get("company"),contentId)
                    print(sql)
                    count = cs1.execute(sql)
                    conn.commit()
                except Exception as e:
                    print("111111111111111111111111111111111TTTTTTTTTTTTTTTTTTTT")
                    print(e)
                    try:
                        with open("error.txt","a")as f:
                            f.write(str(1.1))
                            f.write(" ")
                            f.write(str(contentId))
                            f.write(sql)
                            f.write("\n")
                    except Exception as e:
                        print(e)
        global i
        i=json.loads(response.text).get("data").get("isFinal")
        print(i)
        global j
        if len(json.loads(response.text).get("data").get("commentList")) >= 20:
            j = json.loads(response.text).get("data").get("commentList")[-1].get("timestamp")
            time.sleep(0.1)
    except Exception as e:
        print("111111111111111111111111111111111TTTTTTTTTTTTTTTTTTTT")
        print(e)
        try:
            with open("error.txt", "a")as f:
                f.write(str(1.2))
                f.write(" ")
                f.write(str(contentId))
                f.write(sql)
                f.write("\n")
        except Exception as e:
            print(e)



    while i == False:
        url = "https://content.winbaoxian.com/learning/queryLearningCommentList?timestamp={}&contentId={}&contentType=0&topCommentId=".format(j,contentId)
        try:
            response = requests.get(url, headers=headers, verify=False)
            print(">>>>>>>>>>>>")
            i = json.loads(response.text).get("data").get("isFinal")
            print(response.text)

            # for a in json.loads(response.text).get("data").get("commentList"):
            #     # k.get("data").get("commentList").append(a)
            #     k.append(a)

            for b in json.loads(response.text).get("data").get("commentList"):
                p=copy.deepcopy(l)
                l.add(b.get("userUuid"))

                # print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
                # print(type(b))
                # print(type(json.dumps(b)))
                # print(json.dumps(b))
                # sql = "insert into dailiren(userUuid,cname,company,content,contentId) values('%s','%s','%s','%s',%d)" % (b.get("userUuid"),b.get("cname"),b.get("company"),json.dumps(b, ensure_ascii=False),contentId)

                url1='https://app.winbaoxian.com/card/shared/{}?nw=1'.format(b.get("userUuid"))
                # url1 = 'https://app.winbaoxian.com/card/shared/7bd3a19df63e42e99b1cfb450186e511?nw=1'
                response1 = requests.get(url1, headers=headers, verify=False)
                # print(response1.text)
                data = response1.content.decode('utf8')
                html_data = etree.HTML(data)
                name=html_data.xpath("//section/div[1]/div/h2/text()")
                verify=html_data.xpath("//section/div[2]/div/ul/li[1]/div/span[2]/text()")
                company_add=html_data.xpath("//section/div[2]/div/ul/li[2]/div//text()")
                print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW2222222222222222222222222222222222")
                if re.search(r'：(.*)', "".join(company_add).strip()):
                    q=re.search(r'：(.*)', "".join(company_add).strip()).group(1)
                    print("".join(name).strip(), "".join(verify).strip(),q)

                url2='https://ism.winbaoxian.com/insurance/product/100853/detail?u={}'.format(b.get("userUuid"))
                response2 = requests.get(url2, headers=headers, verify=False)
                s=json.loads(response2.text).get("data").get("mobile")
                # print(json.loads(response2.text).get("data").get("mobile"))
                print(s)

                if len(l)!=len(p):
                    try:
                        sql = "insert into dailiren_copy(userUuid,nickname,company,contentId,name1,verify,company_add,mobile) values('%s','%s','%s',%d,'%s','%s','%s','%s')" % (b.get("userUuid"),b.get("cname"),b.get("company"),contentId,"".join(name).strip(),"".join(verify).strip(),q,s)
                        # sql = "insert into dailiren(userUuid,cname,company,contentId) values('%s','%s','%s',%d)" % (b.get("userUuid"),b.get("cname"),b.get("company"),contentId)
                        print(sql)
                        count = cs1.execute(sql)
                        conn.commit()
                    except Exception as e:
                        print("222222222222222222222222222222TTTTTTTTTTTTTTTTT")
                        print(e)
                        try:
                            with open("error.txt","a")as f:
                                f.write(str(2.1))
                                f.write(" ")
                                f.write(str(contentId))
                                f.write(sql)
                                f.write("\n")
                        except Exception as e:
                            print(e)
            # print(k)
            # print(len(k.get("data").get("commentList")))
            if len(json.loads(response.text).get("data").get("commentList"))>=20:
                j = json.loads(response.text).get("data").get("commentList")[-1].get("timestamp")
                time.sleep(0.1)
        except Exception as e:
                print("222222222222222222222222222222TTTTTTTTTTTTTTTTT")
                print(e)
                try:
                    with open("error.txt", "a")as f:
                        f.write(str(2.2))
                        f.write(" ")
                        f.write(str(contentId))
                        f.write(sql)
                        f.write("\n")
                except Exception as e:
                    print(e)

    # name = ['contentId','commentList']
    # list=[]
    # f=[]
    # # o=[]
    # f.append(contentId)
    # f.append(json.dumps(k))
    # # o.append(json.dumps(k))
    # # list.append(contentId)
    # list.append(f)
    # print("RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRrrr")
    # print(list)
    # test = pd.DataFrame(columns=name, data=list)
    # test.to_csv('./testcsv5.csv',  encoding='utf8',mode='a',header=False)
    # print(k)
    # sql语句,存入数据库



#     if k:
#         with open("content0-1000.txt","a",encoding="utf8") as f:
#             f.write(str(contentId))
#             f.write(",")
#             f.write(json.dumps(k))
#             f.write("\n")
#     print(len(k))
#     print(l)
#     print(len(l))
#     print(contentId)
#     print("-" * 100)
# with open("id0-1000.txt","w")as f:
#     f.write(json.dumps(list(l)))



# import pandas as pd
# list = [[1, 2, 3], [4, 5, 6], [7, 9, 9]]
# # 下面这行代码运行报错
# # list.to_csv('e:/testcsv.csv',encoding='utf-8')
# name = ['one', 'two', 'three']
# test = pd.DataFrame(columns=name, data=list)  # 数据有三列，列名分别为one,two,three
# print(test)
# test.to_csv('e:/testcsv.csv', encoding='gbk')










