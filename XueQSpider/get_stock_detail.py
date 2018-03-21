import datetime
from http import cookiejar
from urllib import request

import pymysql
import requests
import re
import json


# 获取当日财务信息
def get_detail(name):
    params = {
        'symbol': name,
        'page': 1,
        'size': 4,
        '_': datetime.datetime.now()
    }
    url = 'https://xueqiu.com/stock/f10/dailypriceextend.json'
    cookie = get_cookie()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                      '/63.0.3239.108 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'refer': 'https://xueqiu.com/S/' + name + '/MRCWZB'
    }
    r = requests.get(url, params=params, headers=headers, cookies=cookie, timeout=10, verify=False)
    print(r.text)


# 获取当前主要财务指标（季报信息）
def get_financial_report(name):
    params = {
        'symbol': name,
        'page': 1,
        'size': 1,
        '_': datetime.datetime.now()
    }
    url = 'https://xueqiu.com/stock/f10/finmainindex.json?'
    cookie = get_cookie()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                      '/63.0.3239.108 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'refer': 'https://xueqiu.com/S/' + name + '/ZYCWZB'
    }
    r = requests.get(url, params=params, headers=headers, cookies=cookie, timeout=10, verify=False)
    print(r.text)


# 获取cookie方法,通过http.cookiejar包
def get_cookie():
    # 声明一个CookieJar对象实例来保存cookie
    cookie = cookiejar.CookieJar()
    # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    handler = request.HTTPCookieProcessor(cookie)
    # 通过CookieHandler创建opener
    opener = request.build_opener(handler)
    opener.addheaders = [
        ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                       ' Chrome/63.0.3239.108 Safari/537.36')]
    response = opener.open('https://xueqiu.com/S/SH601166')
    # 打印cookie信息
    return cookie


def get_financial_detail():
    pass


def get_stock_brief():
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root", passwd="admin123", db="xueq_data", charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = 'select stock_num from `stock_collect`'
    try:
        # Execute the SQL statement
        cursor.execute(sql)
        stock_name = cursor.fetchmany(100)
        while stock_name:
            for name in stock_name:
                print(name[0])
            break

            # stock_name = cursor.fetchmany(100)
            # get_detail(item[])
    except Exception as e:
        print("Error: ", e)
    # 提交到数据库
    db.commit()
    cursor.close()
    db.close()


if __name__ == '__main__':
    get_stock_brief()
    # get_financial_report('SZ002074')
