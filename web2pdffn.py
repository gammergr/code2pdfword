# coding=utf-8
import os
import re
import time
import logging
import pdfkit
import requests
from bs4 import BeautifulSoup
#解析的网站路径
parserUrl = "https://flutter.cn/docs"
#所解析网站里面的 链接所在点
navItemString = "nav-link"
#解析页面的内容部分，不含 侧边的outline，也就是不包含 侧边栏的那部分，
contentString = "container"

#页面大小设置参考  大的设置A3 普通kindle A5 大小合适， 喜欢看小字可以选letter
page_ref ="""
   QPrinter::A0	5	841 x 1189 mm
    QPrinter::A1	6	594 x 841 mm
    QPrinter::A2	7	420 x 594 mm
    QPrinter::A3	8	297 x 420 mm
    QPrinter::A4	0	210 x 297 mm, 8.26 x 11.69 inches
    QPrinter::A5	9	148 x 210 mm
    QPrinter::A6	10	105 x 148 mm
    QPrinter::A7	11	74 x 105 mm
    QPrinter::A8	12	52 x 74 mm
    QPrinter::A9	13	37 x 52 mm
"""
page_set = "A3"



#
# pattern = "(<img .*?src=\")(.*?)(\")"
# htmltest = """
# <img src="https://flutter.cn/docs/assets/images/docs/development/ui/layout/adaptive_scaffold.gif" class="" alt="">
# """
#
# def func(m):
#     print(m.group(0))
#     print(m.group(1))
#     print(m.group(2))
#     print(m.group(3))
#
#     print("1111")
#
#
#
#
#     if not m.group(3).startswith("http"):
#         rtn = m.group(1) + parserUrl + m.group(2) + m.group(3)
#         return rtn
#     else:
#         return m.group(1) + m.group(2) + m.group(3)
#
# html = re.compile(pattern).sub(func, htmltest)
# print(html)
# exit(1)


def checkValidUrl(li):
    url =""
    print(li)
    if len(li.attrs['class']) == 1 and not 'http' in li.attrs['href'] and not '#' in li.attrs['href']:
        url = parserUrl + li.attrs['href']
    return  url

##############以下部分一般情况不需要修改#################################
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
</head>
<body >
{content}
</body>
</html>
"""


def get_url_list():
    """
    获取所有URL目录列表
    :return:
    """
    response = requests.get(parserUrl)
    soup = BeautifulSoup(response.content, "html.parser")
    menu_tag = soup.find_all(class_=navItemString)
    urls = []
    for li in menu_tag:
        url = checkValidUrl(li)
        if not  len(url) == 0:
            urls.append(url)
    #sort
    addr_to = list(set(urls))
    addr_to.sort(key=urls.index)
    return addr_to


def parse_url_to_html(url, name):
    """
    解析URL，返回HTML内容
    :param url:解析的url
    :param name: 保存的html文件名
    :return: html
    """
    try:
        print("正在解析:"+url)
        # time.sleep(2)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # 正文
        body = soup.find_all(class_=contentString)[0]
        # 标题
        #title = soup.find('h1').get_text()
        # 标题加入到正文的最前面，居中显示
        center_tag = soup.new_tag("center")
        title_tag = soup.new_tag('h1')
        # title_tag.string = title
        center_tag.insert(1, title_tag)
        body.insert(1, center_tag)
        html = str(body)
        # body中的img标签的src相对路径的改成绝对路径
        pattern = "(<img .*?src=\")(.*?)(\")"

        def func(m):
            if not m.group(3).startswith("http"):
                rtn = m.group(1) + parserUrl + m.group(2) + m.group(3)
                return rtn
            else:
                return m.group(1)+m.group(2)+m.group(3)
        html = re.compile(pattern).sub(func, html)
        html = html_template.format(content=html)
        html = html.encode("utf-8")
        with open(name, 'wb') as f:
            f.write(html)
        return name

    except Exception as e:
        logging.error("解析错误", exc_info=True)

def save_pdf(htmls, file_name):
    """
    把所有html文件保存到pdf文件
    :param htmls:  html文件列表
    :param file_name: pdf文件名
    :return:
    Constant	Value	Description
    """
    options = {
        'page-size': page_set,
        'dpi': 70,
        'margin-top': '0.001in',
        'margin-right': '0.001in',
        'margin-bottom': '0.001in',
        'margin-left': '0.001in',
        'encoding': "UTF-8",
        "minimum-font-size":16,
        "disable-internal-links":"",
        "disable-external-links":"",
        "disable-smart-shrinking":"",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'cookie': [
            ('cookie-name1', 'cookie-value1'),
            ('cookie-name2', 'cookie-value2'),
        ],
        'outline-depth': 10,
    }
    pdfkit.from_file(htmls, output_path = file_name, options=options)


def main():
    # get create file name
    try:
        filenameTempString = parserUrl.split("//")[1]
        filenameTempString = filenameTempString.replace(".", "_")
        filenameTempString = filenameTempString.replace("-", "_")
        filenameTempString = filenameTempString.replace("/", "_")
        file_name = filenameTempString + "_" + page_set + ".pdf"
        print("生成文件名:" + file_name)
    except:
        print("确认参数是否正确 parserUrl是网址带http头")
    start = time.time()
    urls = get_url_list()
    htmls = [parse_url_to_html(url, str(index) + ".html") for index, url in enumerate(urls)]
    try:
        save_pdf(htmls, file_name)
    except:
        time.sleep(20)
        print("finish now")
    for html in htmls:
        os.remove(str(html))

    total_time = time.time() - start
    print(u"总共耗时：%f 秒" % total_time)

if __name__ == '__main__':
    main()