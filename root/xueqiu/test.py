import os
import pymysql
import requests
import time

from multiprocessing import Process


def get_open_id():
    # 打开数据库连接
    db = pymysql.connect(host="47.97.217.122", user="root", passwd="admin123", db="fangche", charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = 'select open_id from `log` where coupon_id=39 and `status`=1'
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


def upload(openid):
    print(openid)
    salt = 'otULs0CYGGJfNzTJed2NjJ3LUQhc' + time.time()
    url = 'https://fangche.domobile.net/Api/Redball/play_game'
    # 要上传的文件
    files = {'file': ('40504.mp3', open('E:/python-workspace/testupload/40500.mp3', 'rb'))}  # 显式的设置文件名

    # post携带的数据
    data = {'open_id': openid,
            'salt': salt,
            'nickname': '肥猫',
            'avatar': 'https://wx.qlogo.cn/mmopen/vi_32'
                      '/Q0j4TwGTfTKYpcrO6tvQSdlibJiaNFPVzl4d2BP0rQKl0cc31xYF1iaPKlJ0elJSLqG7mBVHngV7H284KCUQYOxKA/0',
            'voice_time': 4,
            'create_time': time.time(),
            'coupon_id': 162
            }

    r = requests.post(url, files=files, data=data)
    if r.status_code == 200 & r.json()['code'] == 200:
        #  调用查询
        j = 0
        while j < 5:
            result = get_result(salt=salt)
            if result:
                j = j + 1
        pass
    else:
        pass
    print('child process %s is over...' % os.getpid())


def get_result(salt):
    result = requests.get('https://fangche.domobile.net/Api/Redball/getInfoBySalt?salt=' + salt)
    return result.status_code == 200


def test_redball_time(time):
    data = {
        'redball_id': 1,
        'time': time
    }
    r = requests.post('https://fangche.domobile.net/Api/Lottery/test_get_redball', data=data)
    print(r.text)


if __name__ == '__main__':
    time = int(time.time())
    for i in range(50):
        test_redball_time(time)
        time += 60
