import sys
def Factorial(num):
    if num == 1 :
        return 1
    else:
        result = num * Factorial(num-1)
        return result
if __name__ == '__main__' :
    result = Factorial(5)
    print('5的阶乘是：{}'.format(result))