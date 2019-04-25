import os
from PIL import Image, ImageEnhance
from selenium import webdriver
import time
from requests.exceptions import RequestException
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
# '使用phantomJS'
# phantomjs_path = r'phantomjs'
# driver = webdriver.PhantomJS(executable_path=phantomjs_path)

# 使用chrome浏览器
driver = webdriver.Chrome()
# 使用chrome时要注意，chromedriver与chrome版本要匹配，请按照这个表：https://blog.csdn.net/huilan_same/article/details/51896672
# 设置浏览器窗口位置及大小
driver.set_window_rect(x=0, y=0, width=1350, height=748)
# 设定页面加载限制时间
driver.set_page_load_timeout(30)


# 设置锁定标签等待时长
# wait = WebDriverWait(driver, 20)

# TESSERACT_PATH = 'E:\Program Files (x86)\Tesseract-OCR\\tesseract.exe'


def tesseract(filename, output):
    # 调用tesseract进行文字数字识别，目前对于浅颜色的字体识别率较低，若想提高识别率需要对图片做预处理
    os.system('echo off')  # 关闭命令行窗口运行命令的显示
    os.system('tesseract' + ' ' + filename + ' ' + output + ' ' + '-l num+chi_tra')  # 默认已配置好系统变量
    time.sleep(2)
    f = open(output + ".txt", encoding='utf-8')
    try:
        t = f.readlines()[0]
    except IndexError:
        t = '未识别'
    f.close()
    return t


def analysis_pic(div, length, n):
    # chrome浏览器只能保存当前展示的网页，对于现在不能显示部分我们就截取不到，这时候我们需要利用js操作，下拉网页，
    # 保存当前窗口为图片
    driver.save_screenshot('b.png')
    # time.sleep(2)
    # 定位div地址
    location = div.location
    # print(location)
    # 得到div尺寸
    size = div.size
    # print(size)
    left = location['x']
    top = location['y'] - length
    right = location['x'] + size['width']
    bottom = location['y'] + size['height'] - length
    a = Image.open("b.png")
    im = a.crop((left, top, right, bottom))
    im.save("raw_a{}.png".format(n))
    imgry = im.convert('L')  # 图像加强，二值化
    sharpness = ImageEnhance.Contrast(imgry)  # 对比度增强
    sharp_img = sharpness.enhance(2.0)
    sharp_img.save("a{}.png".format(n))
    # im.save('a.png')
    num = tesseract("a{}.png".format(n), 'a')
    return num


def get_parse_page(url):
    # 新生成一个DataFrame的变量保存爬取到的数据
    df = pd.DataFrame({})
    try:
        driver.get(url)
        time.sleep(3)
        contents_list = driver.find_elements_by_css_selector('dl.board-wrapper dd')
        contents = {}
        # n和length为不断下拉页面的参数
        n = 1
        length = 0
        for content in contents_list:
            try:
                contents['index'] = content.find_element_by_css_selector('i.board-index').text
                contents['image_url'] = content.find_element_by_css_selector('img.board-img').get_attribute('src')
                contents['title'] = content.find_element_by_css_selector('img.board-img').get_attribute('alt')
                try:
                    contents['actor'] = content.find_element_by_css_selector('p.star').text
                except NoSuchElementException:
                    contents['actor'] = ''
                contents['time'] = content.find_element_by_css_selector('p.releasetime').text
                png = content.find_elements_by_css_selector('span.stonefont')[0]
                # print(png.text)

                contents['real_time'] = analysis_pic(png, length, n).strip() + \
                                        content.find_element_by_css_selector('p.realtime').text[-1]

                png = content.find_elements_by_css_selector('span.stonefont')[1]
                # print(png.text)
                # contents['total_booking'] = analysis_pic(png, length, n).strip() + content.find_element_by_css_selector('p.total-boxoffice').text[-1]
                contents['record_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

                print(contents)
                df = df.append(contents.copy(), ignore_index=True)
                length = n * 270
                driver.execute_script('window.scrollTo(0, {}*270)'.format(n))
                n = n + 1
            except NoSuchElementException:
                pass
        return df
    except RequestException:
        print('出错啦')
        return None


def main():
    url = 'http://maoyan.com/board/1'
    info = get_parse_page(url)
    info.to_csv(r'movies_info.csv', encoding='utf-8')
    driver.close()


if __name__ == '__main__':
    main()