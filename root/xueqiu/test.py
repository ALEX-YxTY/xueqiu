import os
import datetime

import pymysql
import requests
import time

from multiprocessing import Process


def get_open_id():
    # 打开数据库连接
    db = pymysql.connect(host="47.97.217.122", user="root", passwd="admin123", db="fangche", charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = 'select open_id from `user` limit 800,400'

    try:
        # Execute the SQL statement
        cursor.execute(sql)
        open_list = cursor.fetchall()
        return open_list

    except Exception as e:
        print("Error: ", e)
    # 提交到数据库
    db.commit()
    cursor.close()
    db.close()


def upload(openid, index):
    salt = openid + str(int(time.time()))
    url = 'https://fangche.domobile.net/Api/Fball/play_game'
    # 要上传的文件
    files = {'file': ('40504.mp3', open('E:/python-workspace/testupload/40500.mp3', 'rb'))}  # 显式的设置文件名

    # post携带的数据
    data = {'open_id': openid,
            'salt': salt,
            'nickname': '肥猫' + str(index),
            'avatar': 'https://wx.qlogo.cn/mmopen/vi_32'
                      '/Q0j4TwGTfTKYpcrO6tvQSdlibJiaNFPVzl4d2BP0rQKl0cc31xYF1iaPKlJ0elJSLqG7mBVHngV7H284KCUQYOxKA/0',
            'voice_time': 4,
            'create_time': int(time.time()),
            'coupon_id': 848,
            'channel_id': 848,
            'redball_id': 4
            }

    r = requests.post(url, files=files, data=data)
    if r.status_code == 200 & r.json()['code'] == 200:
        #  调用查询
        j = 0
        while j < 1:
            result = get_result(salt, openid[0])
            if result:
                j = j + 1
        pass
    else:
        pass
    print('child process %s is over...' % os.getpid())


def get_result(salt, open_id):
    url = 'https://fangche.domobile.net/Api/Fball/getInfoBySalt?salt=' + salt + '&open_id=' + open_id
    result = requests.get(url)
    return result.status_code == 200


def change_redball_time():
    # 打开数据库连接
    db = pymysql.connect(host="47.97.217.122", user="root", passwd="admin123", db="fangche", charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = ''
    time_start = datetime.datetime.strptime("2018-04-18 09:00:00", '%Y-%m-%d %H:%M:%S')
    time_end = datetime.datetime.strptime("2018-04-18 22:00:00", '%Y-%m-%d %H:%M:%S')

    for i in range(100):
        index = 848 + i
        start = time_start + datetime.timedelta(days=(i // 10))
        end = time_end + datetime.timedelta(days=(i // 10))
        sql += "update `enterprise_redball` set  start_time=%d,end_time=%d WHERE `id`=%d ;" % (
            int(start.timestamp()), int(end.timestamp()), index)
    try:
        # Execute the SQL statement
        cursor.execute(sql)
    except Exception as e:
        print("Error: ", e)
    # 提交到数据库
    db.commit()
    cursor.close()
    db.close()


if __name__ == '__main__':
    # open_list = get_open_id()
    # i = 0
    # while i < open_list.__len__():
    #     process = Process(target=upload, args=(open_list[i][0], i))
    #     print('Child ' + process.name + 'process will start.')
    #     process.start()
    #     i += 1
    change_redball_time()
