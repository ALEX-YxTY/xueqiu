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
            max_money_avalible = t_money / t_num * times
            if max_money_avalible > suplus_money:
                max_money_avalible = suplus_money
            money = max_money_avalible * (random.random() ** (times / 2))
        if money < 0.01:
            money = 0.01
        suplus_num -= 1
        suplus_money -= money
        total_money += money
        if money > max_money:
            max_money = money
            max_id = t_num - suplus_num
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
    # print('总计花费：%f' % total_money)
    # print('小于0.5元比例：%f' % (count1 / t_num))
    # print('0.5-1元比例：%f' % (count2 / t_num))
    # print('1-1.5元元比例：%f' % (count3 / t_num))
    # print('1.5-2元比例：%f' % (count4 / t_num))
    # print('大于2元比例：%f' % (count5 / t_num))
    # print('最大金额为：%f' % max_money)
    print('最大金额产生在第 %d 位' % max_id)
    return max_id

    # print(datetime.datetime.now() - time)


if __name__ == '__main__':
    total_id = 0
    for i in range(100):
        max_id = distribution_1(200, 200, 6)
        total_id += max_id
    print('平均最多位数：%d' % (total_id / 100))
