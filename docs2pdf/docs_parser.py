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
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body >
{content}
</body>
</html>
"""
class DocsParser:
    _url=""
    _contentHead=""
    _itemTag = ""
    _pageSize = ""
    _imgOffset = ""

    def __init__(self,url,contentHead,itemTag,pageSize):
        print("要解析的网址:"+url)
        print("默认 图片偏移地址是上面的url，如果有偏移请调用setImgOffset 相对的path的头例如设置为域名")
        print("正文内容标签，不包含侧边栏："+contentHead)
        print("侧边栏的超链接包含的项："+itemTag)
        self._url = url
        self._contentHead = contentHead
        self._itemTag = itemTag
        self._pageSize = pageSize
        self._imgOffset = url

    def createSaveFileName(self):
        file_name = ""
        try:
            filenameTempString = self._url.split("//")[1]
            filenameTempString = filenameTempString.replace(".", "_")
            filenameTempString = filenameTempString.replace("-", "_")
            filenameTempString = filenameTempString.replace("/", "_")
            file_name = filenameTempString + "_" + self._pageSize + ".pdf"
        except:
            print("确认参数是否正确 parserUrl是网址带http头")
        print("生成的文件名为："+file_name)
        return file_name

    def setImgOffset(self,imgOffset):
        print("设置 文中的图片的相对路径的域名")
        self._imgOffset = imgOffset

    def parserHtml(self,url,name):
        try:
            print("正在解析 item:" + url)
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            # 正文
            body = soup.find_all(class_=self._contentHead)[0]
            # 标题
            # title = soup.find('h1').get_text()
            print("----------------")
            print(soup.find('h1').get_text())
            print("----------------")
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
                if not m.group(2).startswith("http"):
                    rtn = m.group(1) + self._imgOffset + m.group(2) + m.group(3)
                    return rtn
                else:
                    return m.group(1) + m.group(2) + m.group(3)

            html = re.compile(pattern).sub(func, html)
            html = html_template.format(content=html)
            html = html.encode("utf-8")
            with open(name, 'wb') as f:
                f.write(html)
            return name

        except Exception as e:
            logging.error("解析错误", exc_info=True)

    def checkValidUrl(self,li):
        print("!!!可能需要根据不同项目重写的函数 checkValidUrl!!!")
        url = ""
        if len(li.attrs['class']) == 1 and not 'http' in li.attrs['href'] and not '#' in li.attrs['href']:
            url = self._url + li.attrs['href']
        return url

    def getUrlList(self):
        print("获取所需URL中所有item链接")
        response = requests.get(self._url)
        soup = BeautifulSoup(response.content, "html.parser")
        menu_tag = soup.find_all(class_=self._itemTag)
        urls = []
        for li in menu_tag:
            urlTemp = self.checkValidUrl(li)
            if not len(urlTemp) == 0:
                urls.append(urlTemp)

        addr_to = list(set(urls))
        addr_to.sort(key=urls.index)
        return addr_to

    def save_pdf(self,htmls):
        print("保存到文件 ")
        options = {
            'page-size': self._pageSize,
            'dpi': 70,
            'margin-top': '0.001in',
            'margin-right': '0.001in',
            'margin-bottom': '0.001in',
            'margin-left': '0.001in',
            'encoding': "UTF-8",
            "minimum-font-size": 16,
            "disable-internal-links": "",
            "disable-external-links": "",
            "disable-smart-shrinking": "",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'outline-depth': 10,
        }
        pdfkit.from_file(htmls, output_path=self.createSaveFileName(), options=options)


    def process(self):
        print("开始处理 计时开始")
        start = time.time()
        urls = self.getUrlList()
        htmls = [self.parserHtml(url, str(index) + ".html") for index, url in enumerate(urls)]
        try:
            #self.save_pdf(htmls)
            pass
        except:
            time.sleep(10)#避免异常delay
            print("转换完成")


        for index in range(len(htmls)-1):
            print(htmls[index])
            cmd = "copy "+htmls[index]+"+"+htmls[index+1] +" temp.html /Y"
            # print(cmd)
            os.system(cmd)
            cmd = "copy  temp.html "+htmls[index+1]+"/Y"
            # print(cmd)
            os.system(cmd)

        for html in htmls:
            os.remove(str(html))

        total_time = time.time() - start
        print(u"总共耗时：%f 秒" % total_time )
        print(u"总共：%d个链接" %  len(htmls))

