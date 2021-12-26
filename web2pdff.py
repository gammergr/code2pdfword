# coding=utf-8
import os
import re
import time
import logging
import pdfkit
import requests
from bs4 import BeautifulSoup

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>

"""


def parse_url_to_html(url, name):
    """
    解析URL，返回HTML内容
    :param url:解析的url
    :param name: 保存的html文件名
    :return: html
    """
    print(name + "  " + url)
    # time.sleep(9)
    print(name +"  "+url +"  end")
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        print(url)
        # 正文
        body = soup.find_all(class_="container")[0]
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
                rtn = m.group(1) + "https://docs.flutter.dev" + m.group(2) + m.group(3)
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


def get_url_list():
    """
    获取所有URL目录列表
    :return:
    """
    count = 0
    response = requests.get("https://docs.flutter.dev")
    soup = BeautifulSoup(response.content, "html.parser")
    # print(response.content)
    menu_tag = soup.find_all(class_="nav-link")

    # countn=0
    # for x in menu_tag:
    #     print(len(x.attrs['class']))
    #     if len(x.attrs['class']) ==1:
    #         menu_tagn[countn] = x
    #         countn = countn +1


    urls = []
    for li in menu_tag:
        # print(len(li.attrs['class']))

        if len(li.attrs['class']) ==1 and not  'http' in li.attrs['href'] and not '#' in li.attrs['href']:
            url = "https://docs.flutter.dev" + li.attrs['href']
            urls.append(url)
            print(url)
            count = count + 1
            # if count > 98:
            #     break

    print(str(count)+"个url")
    return urls


def save_pdf(htmls, file_name):
    """
    把所有html文件保存到pdf文件
    :param htmls:  html文件列表
    :param file_name: pdf文件名
    :return:
    """
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
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
    start = time.time()
    urls = get_url_list()
    file_name = "dartchina.pdf"
    htmls = [parse_url_to_html(url, str(index) + ".html") for index, url in enumerate(urls)]
    save_pdf(htmls, file_name)

    for html in htmls:
        os.remove(html)

    total_time = time.time() - start
    print(u"总共耗时：%f 秒" % total_time)


if __name__ == '__main__':
    main()