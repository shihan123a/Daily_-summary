# 猜数字
# !/usr/bin/python
# -*- coding: utf-8 -*-
import random


def new_guess():  # 定义每次猜测的一个1-100之间的随机数
    number = random.randint(0, 100)
    # print(number)
    return number


def new_game():
    number = new_guess()  # 首轮游戏默认随机数为猜测数字，在指定次数内猜对重新生成。
    n = 0
    while True:
        n += 1  # 统计一共游戏的次数
        try:
            guess_num = int(input('请输入你要尝试的次数：'))
        except ValueError:
            guess_num = 10
        print('输入的次数不合法，默认最多猜10次')
        for i in range(guess_num):
            guess = int(input('请输入你猜的数字：'))
            if guess > number:
                print('你猜的数字大了，不要灰心，继续加油！')
            elif guess < number:
                print('你猜的数字小了，不要灰心，继续努力！')
            else:
                if i < 3:
                    print('真厉害，这么快就猜对了！')
                else:
                    print('终于猜对了，恭喜恭喜！')
                    number = new_guess()  # 猜对后将调用生成函数再次生成新的数字
                    break

                if i == guess_num - 1:
                    print('很遗憾！在{}次中你均未猜出'.format(guess_num))
                    next_game = input('是否继续游戏？请输入 yes or no：')
                if next_game == 'no':  # 根据用户输入判断是否开始新一轮游戏
                    break
                else:
                    print('开始下一轮游戏！')

                    continue
                    print('你一共玩了{}轮游戏哦'.format(n))


if __name__ == '__main__':
    print('猜数字小游戏!')
    new_game()
