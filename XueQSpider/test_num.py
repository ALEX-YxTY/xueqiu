import random
import datetime


def distribution_1(t_money, t_num, times):
    time = datetime.datetime.now()

    total_money = 0
    suplus_num = t_num
    suplus_money = t_money
    count1 = count2 = count3 = count4 = count5 = 0
    max_money = 0

    while suplus_num > 0:
        if suplus_num == 1:
            money = suplus_money
        else:
            money = suplus_money / suplus_num * times * (random.random() ** (times / 2+1))
        if money < 0.01:
            money = 0.01
        suplus_num -= 1
        suplus_money -= money
        total_money += money
        if money > max_money:
            max_money = money
        if money < 0.5:
            count1 += 1
        elif money <= 1:
            count2 += 1
        elif money < 1.5:
            count3 += 1
        elif money < 2:
            count4 += 1
        else:
            count5 += 1
    print('总计花费：%f' % total_money)
    print('小于0.5元比例：%f' % (count1 / 10000))
    print('0.5-1元比例：%f' % (count2 / 10000))
    print('1-1.5元元比例：%f' % (count3 / 10000))
    print('1.5-2元比例：%f' % (count4 / 10000))
    print('大于2元比例：%f' % (count5 / 10000))
    print('最大金额为：%f' % max_money)
    print(datetime.datetime.now() - time)


if __name__ == '__main__':
    distribution_1(20000, 10000, 10)
