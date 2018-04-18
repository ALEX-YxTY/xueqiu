from datetime import datetime
import pymysql
from HttpRequest import HttpRequest
import json


# 获取股票代码列表
# from 和讯  url = 'http://quote.tool.hexun.com/hqzx/quote.aspx'


def get_stock_name():
    print("start time:%f" % (datetime.now().timestamp()))
    number = 1  # 初始化页码，后续修改
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root", passwd="admin123", db="xueq_data", charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 初始化header连接对象
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/63.0.3239.108 Safari/537.36'}
    # 和讯行情中心 沪深 股票列表查询接口 GET
    url = 'http://quote.tool.hexun.com/hqzx/quote.aspx'
    i = 0

    while i < number:
        print('%.2f' % ((i + 1) / number * 100))
        data = {
            # type
            'type': 2,
            # market
            'market': 0,
            # sortType 排序类型,即排序的字段序号
            'sorttype': 0,
            # updown 升降序
            'updown': 'down',
            # page 页码
            'page': i + 1,
            # count 每页显示数目
            'count': 100,
            # time
            'time': 224220 + i * 20
        }
        response = HttpRequest.get(url, data=data)
        response = response.strip("dataArr = ")
        if number == 1:
            # 修改页面总数
            number = int(response[response.find("dataArr,") + 8:-24])
            print(number)
        response = '{ \"arr\":' + response[:response.find(";")] + '}'
        json_load = json.loads(response.replace('\'', '\"'))

        sql = """insert into `stock_collect`(`stock_type`,`stock_num`,`stock_name`)values"""

        for item in json_load["arr"]:
            data = []
            num = item[0]
            if num.startswith('6'):
                # 沪市主板
                data.insert(0, 0)
                data.insert(1, 'SH' + num)
            elif num.startswith('000'):
                # 深市主板
                data.insert(0, 1)
                data.insert(1, 'SZ' + num)
            elif num.startswith('002'):
                # 深市中小板
                data.insert(0, 3)
                data.insert(1, 'SZ' + num)
            else:
                # 创业板
                data.insert(0, 4)
                data.insert(1, 'SZ' + num)
            sql += "('%s', '%s','%s')," % (data[0], data[1], item[1])
        sql = sql[:-1]
        try:
            # Execute the SQL statement
            cursor.execute(sql)
        except Exception as e:
            print("Error: ", e)
        # 提交到数据库
        db.commit()
        # 更新i
        i += 1

    cursor.close()
    # 关闭数据库连接
    db.close()
    print("end time:%f" % (datetime.now().timestamp()))


# 获取股票详情
# from 雪球 url='https://xueqiu.com/v4/stock/quote.json?code=SZ002741'
# user-agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome
# /63.0.3239.108 Safari/537.36'
def get_stock_detail_by_name(result):
    url = 'https://xueqiu.com/v4/stock/quote.json'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/63.0.3239.108 Safari/537.36'}
    data = {
        # 股票代码
        'code': result
    }
    request_get = HttpRequest.get(url, data, header=header, decode='utf8')
    print(request_get)


def get_stock_detail():
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root", passwd="admin123", db="xueq_data", charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = """SELECT `stock_num` FROM `stock_collect` LIMIT 1 """
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    for result in data:
        get_stock_detail_by_name(result[0])


if __name__ == '__main__':
    # get_stock_detail()
    get_stock_name()
