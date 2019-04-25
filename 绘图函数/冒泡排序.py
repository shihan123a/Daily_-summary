# python 冒泡排序

def paixu(li) :
    max = 0
    for ad in range(len(li) - 1):
        for x in range(len(li) - 1 - ad):
            if li[x] > li[x + 1]:
                max = li[x]
                li[x] = li[x + 1]
                li[x + 1] = max
            else:
                max = li[x + 1]
    print(li)
paixu([41,23344,9353,5554,44,7557,6434,500,2000])