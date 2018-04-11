import datetime
import time
from http import cookiejar
from urllib import request

import pymysql
import requests
import re
import json

# 获取当日财务信息
from urllib3.exceptions import InsecureRequestWarning


def get_detail(name, cookies):
    params = {
        'symbol': name,
        'page': 1,
        'size': 4,
        '_': time.time()
    }
    url = 'https://xueqiu.com/stock/f10/dailypriceextend.json'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                      '/63.0.3239.108 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'refer': 'https://xueqiu.com/S/' + name + '/MRCWZB'
    }
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    r = requests.get(url, params=params, headers=headers, cookies=cookies, timeout=10, verify=False)
    result = r.text
    r.close()
    return json.loads(result)['tqQtSkdailypriceExtend']


# 获取当前主要财务指标（季报信息）
def get_financial_report(name, cookies):
    params = {
        'symbol': name,
        'page': 1,
        'size': 1,
        '_': datetime.datetime.now()
    }
    url = 'https://xueqiu.com/stock/f10/finmainindex.json?'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                      '/63.0.3239.108 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'refer': 'https://xueqiu.com/S/' + name + '/ZYCWZB'
    }
    r = requests.get(url, params=params, headers=headers, cookies=cookies, timeout=10, verify=False)
    return json.loads(r.text)


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
    opener.close()
    # 打印cookie信息
    return cookie


def get_stock_brief(cookies):
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root", passwd="admin123", db="xueq_data", charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    cursor2 = db.cursor()
    sql = 'select stock_num from `stock_collect`'
    try:
        # Execute the SQL statement
        cursor.execute(sql)
        stock_name = cursor.fetchall()
        time_start = time.time()
        i = 0
        insert_sql = """insert into `s_record_1`(`stock_name`,`date`,`topen`,`tclose`,`thigh`,`tlow`,`amount`,`vol`,`change`,`pchg`
    ,`amplitude`,`avgprice`,`tmc`,`famc`,`pettm`,`pelyr`,`pettm_kf`,`pelyr_kf`,`pb`,`pslyr`,`psttm`,`dyr`,`evps`)values"""
        for name in stock_name:
            i += 1
            stock_daily = get_detail(name[0], cookies)
            daily_rep = stock_daily['tqQtSkdailyprice']
            daily_fin = stock_daily['tqSkFinindic']
            insert_sql_else = "('%s', '%d', '%.2f', '%.2f', '%.2f', '%.2f', '%.2f', '%d', '%.2f','%.2f','%.2f','%.2f','%.2f','%.2f'" \
                              ",'%.2f','%.2f','%.2f','%.2f','%.2f','%.2f','%.2f','%.2f','%.2f')" % (
                                  name[0], int(daily_rep['tradedate']), daily_rep['topen'],
                                  daily_rep['tclose'], daily_rep['thigh'], daily_rep['tlow'],
                                  daily_rep['amount'], daily_rep['vol'], daily_rep['change'],
                                  daily_rep['pchg'], daily_rep['amplitude'], daily_rep['avgprice'],
                                  daily_rep['totmktcap'], daily_rep['negotiablemv'],
                                  [daily_fin['pettm'], 0.0][daily_fin['pettm'] is None],
                                  [daily_fin['pelfy'], 0.0][daily_fin['pelfy'] is None],
                                  [daily_fin['pettmnpaaei'], 0.0][daily_fin['pettmnpaaei'] is None],
                                  [daily_fin['pelfynpaaei'], 0.0][daily_fin['pelfynpaaei'] is None],
                                  daily_fin['pb'], [daily_fin['pslfy'], 0.0][daily_fin['pslfy'] is None],
                                  [daily_fin['psttm'], 0.0][daily_fin['psttm'] is None],
                                  [daily_fin['dy'], 0.0][daily_fin['dy'] is None],
                                  [daily_fin['evps'], 0.0][daily_fin['evps'] is None])
            print('now come %s and %d' % (name[0], i))
            try:
                cursor2.execute(insert_sql + insert_sql_else)
            except Exception as e:
                print('Exception2:', e)
        # if i % 100 == 0:
            time.sleep(1)
        #         insert_sql = insert_sql[:-1]
        #         try:
        #             cursor2.execute(insert_sql)
        #             insert_sql = """insert into `s_record_1`(`stock_name`,`date`,`topen`,`tclose`,`thigh`,`tlow`,`amount`,`vol`,`change`,`pchg`
        #                         ,`amplitude`,`avgprice`,`tmc`,`ftmc`,`pettm`,`pelyr`.`pettm_kf`,`pelyr_kf`,`pb`,`pslyr`,`psttm`,`dyr`,`evps`)values"""
        #             print('now %d has finished and now is %s' % (i // 100, name[0]))
        #         except Exception as e:
        #             print("Error2: ", e)
        # insert_sql = insert_sql[:-1]
        # try:
        #     cursor2.execute(insert_sql)
        #     print('now all have finished')
        # except Exception as e:
        #     print("Error3: ", e)
        time_end = time.time()
        print('all finish cost: %d' % (time_end - time_start))
    except Exception as e:
        print("Error: ", e)
    # 提交到数据库
    db.commit()
    cursor.close()
    cursor2.close()
    db.close()


if __name__ == '__main__':
    cookie = get_cookie()
    get_stock_brief(cookie)
