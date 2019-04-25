# -*- coding: utf-8 -*-
# 作者:shihan

# 首先引入以下库
import os
import re
import pandas as pd
import requests


def get_page_html(url):
    # 获取目标网站的HTML的函数
    try:
        r = requests.get(url)
        r.raise_for_status()
        # 该语句实在获取到的内容出现乱码时才加入到程序中的，这里没有出现乱码，反而加入后出现了乱码所以注释掉了
        # r.encoding = r.apparent_encoding
        return r.text
    except Exception as e:
        print("爬取失败，错误为：" + str(e) + "/n出错的url：" + url)
        return None


def parse_page(html):
    # 分析页面内容的函数
    # 由于每个网页有多条房屋出租的信息，每条信息用字典保存，整个网页信息用列表保存，所以下面先定义一个空字典和空列表
    info_dict = {}
    info_list = []
    try:
        # 首先把找到记录每条租房信息的HTML标签，findall函数可以以列表形式返回匹配到的所有内容，如何不成功返回None，中间用到了.*?非贪婪匹配模式
        texts = re.findall(r'''<dd class="listItem clearfix.*?</dd>''', html, re.S)
    except:
        texts = None
        print('解析出现了问题请检查')
    # 接下来要判断是否获取到了每条租房信息
    if texts:
        # 然后循环处理获取到的租房信息的标签
        for text in texts:
            # 首先提取URL，因为每个标签里面只有一条信息，所以可以使用search函数，该函数匹配不成功会返回None，我们需要的url在a标签的href中，以双引号作为前后标识，用.*?匹配url并用小括号括起来，这样便可提取出url。
            url = re.search(r'''<h3 class="name"><a href="(.*?)" target="_blank">''', text, re.S)
            # if语句判断是否匹配成功，若未成功利用continue关键字跳过for循环内的其他语句，进入下一个循环中。
            if url:
                info_dict['URL'] = url.group(1)
            else:
                continue

            # 注意[]和*号的用法，同时注意在.前加了一个转义符
            price = re.search(r'<span class="number">([\d\.]*)</span>', text, re.S)
            # print(price.groups())
            if price:
                info_dict['租金'] = price.group(1)
            else:
                continue
            # [\u4e00-\u9fa5]*?之所以不写为.*?,是因为写为后者会匹配到其他内容，大家可尝试一下；(\d*).*?住房面积这里后面是面积单位解析出来是乱码，所以就用小括号内贪婪匹配，后面非贪婪匹配这样就可以只得到数字；\s*(.*?)记录户型的代码中有大量空格、制表符、换行符等空白字符，可以用\s*对其进行匹配；
            way_of_rents = re.search(
                r'''<div class="item">([\u4e00-\u9fa5]*?)<span class="fg">/</span>(\d*).*?<span class="fg">/</span>\s*(.*?)<span class="fg">''',
                text, re.S)
            # print(way_of_rents.groups())
            if way_of_rents:
                info_dict['租赁方式'] = way_of_rents.group(1)
                info_dict['房间面积'] = way_of_rents.group(2)
                info_dict['户型'] = way_of_rents.group(3)
            else:
                continue

            address = re.search(
                r'''<a href=.*?target='_blank' class='link'>(.*?)</a> <span class="fg">/</span>(.*?)\s*<a class="mapimg"''',
                text, re.S)
            # print(address.groups())
            if address:
                info_dict['小区名称'] = address.group(1)
                info_dict['详细地址'] = address.group(2)
            else:
                continue
            # 最后用列表的append方法将获取到的租房信息添加到列表中，这里一定要注意使用copy函数,对字典进行浅复制，详细了解请看：http://www.runoob.com/w3cnote/python-understanding-dict-copy-shallow-or-deep.html
            info_list.append(info_dict.copy())
        # print('info_list:', info_list)
        return info_list


def save_infos(info_lists, kw):
    # 保存获取到的数据
    # 给出存放抓取内容的路径，如果不存在新生成该文件夹
    house365path = r'D:\Python练习题\demo02\summary\house淘房'
    if not os.path.isdir(house365path):
        os.mkdir(house365path)
    # 将获取到的数据保存起来
    info_lists.to_csv(house365path + r'\{}.csv'.format(kw))


def main():
    # 主函数，调用get_page_html和parse_page完成爬取任务
    # 获取的关键字，这里是地点名
    kw = '雨花台'
    # 给出爬取深度，这里爬前三页
    page_num = range(1, 4)
    # 生成DataFrame类型变量，因为该类型数据可以直接保存为CSV格式文件
    info_lists = pd.DataFrame({})
    base = "http://nj.rent.house365.com/district/dl_j2-p{pagenum}-kw{kw}.html"
    for i in page_num:
        # 得到完整url
        url = base.format(pagenum=i, kw=kw)
        if url:
            # 获取HTML
            html = get_page_html(url)
        if html:
            # 获取租房信息的列表格式数据
            info_list = parse_page(html=html)
        if info_list:
            # 将得到的数据添加到DataFrame类型变量中
            info_lists = info_lists.append(info_list, ignore_index=True)
    print(info_lists)
    # 将获取到的数据保存起来
    save_infos(info_lists, kw)


if __name__ == '__main__':
    main()

