import os.path
import re
import time
import urllib
import os

from bs4 import BeautifulSoup

import  docs_parser

#解析的网站路径
parserUrl = "https://flutter.cn/docs"
parserUrl = "https://dart.cn/guides"
imgOffset = "https://dart.cn"
#所解析网站里面的 链接所在点
navItemString = "nav-link"
navItemString = "nav-item"

#解析页面的内容部分，不含 侧边的outline，也就是不包含 侧边栏的那部分，
contentString = "container"
contentString = "content"


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



class testDartcn(docs_parser.DocsParser):

   def checkValidUrl(self, li):
      url=""
      if not 'http' in li.a.get('href') and not '#' in li.a.get('href'):
         url = imgOffset + li.a.get('href')
      return url



class testFluttercn(docs_parser.DocsParser):
   pass







# docsParser = testDartcn(parserUrl, contentString, navItemString, page_set)
# docsParser.setImgOffset(imgOffset)
# docsParser.process()

#
#
temp = testFluttercn("https://flutter.cn/docs","container","nav-link","A3")
temp.process()

with open("temp.html",'rb') as f:
   content = f.read()

soup = BeautifulSoup(content, 'html.parser')
# 正文

localImgs=[]
imglist = soup.find_all('img')  #发现html中带img标签的数据，输出格式为<img xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx，存入集合
lenth = len(imglist)  #计算集合的个数
for i in range(lenth):
  print( imglist[i].attrs['src'])
  if "https://flutter.cn/docs" in imglist[i].attrs['src']:
      print(imglist[i].attrs['src'].split("https://flutter.cn/docs")[1])
      localImgs.append(imglist[i].attrs['src'].split("https://flutter.cn/docs")[1])


lenth = len(localImgs)  #计算集合的个数
for i in range(lenth):
   # print(os.path.splitdrive(os.getcwd() + "/" + os.path.dirname(localImgs[i])))
   if not  os.path.exists(os.getcwd()+"\\"+os.path.dirname(localImgs[i]).replace("/","\\")):
      os.makedirs(os.getcwd()+"\\"+os.path.dirname(localImgs[i]).replace("/","\\"))

    #img
   imgAdd =  "https://flutter.cn/docs"+localImgs[i]

   print(imgAdd)
   urllib.request.urlretrieve(imgAdd, os.getcwd()+os.path.dirname(localImgs[i]).replace("/","\\")+"\\"+os.path.basename(localImgs[i]))

   print(os.getcwd()+os.path.dirname(localImgs[i]).replace("/","\\")+"\\"+os.path.basename(localImgs[i]))

with open("temp.html", "r",encoding='utf-8') as f:
    contentString = f.read()
contentStringProcess = str(contentString).replace(".svg","svg")
contentStringProcess = contentStringProcess.replace("https://flutter.cn/docs",".")
with open(temp.createSaveFileName().replace(".pdf",".html"), "w",encoding='utf-8') as f:
    f.write(contentStringProcess)


os.system(".\kindlegen_win32_v2_9\kindlegen "+temp.createSaveFileName().replace(".pdf",".html"))