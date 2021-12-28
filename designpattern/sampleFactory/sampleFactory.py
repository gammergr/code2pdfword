import abc
from abc import *


class BookInfo(object):
    url = ""
    navItemContent = ""
    content = ""

    def __init__(self, url, navItem, content):
        self.url = url
        self.navItemContent = navItem
        self.content = content


class Book(metaclass=abc.ABCMeta):
    bookInfo = ""
    fileExtension = ""
    name = ""

    def __init__(self, bookInfo, fmt):
        self.bookInfo = bookInfo
        self.fileExtension = "." + fmt
        self.name = self.calcBookName(fmt)
        self.prepare()

    @abstractmethod
    def makeBook(self):
        '''
        makeBook
        :制作电子书:
        '''

    def calcBookName(self,fmt):
        '''
        从参数里面计算出书的名字
        :return:
        '''
        print(self.bookInfo.url)
        filenameTempString = self.bookInfo.url.split("//")[1]
        filenameTempString = filenameTempString.replace(".", "_")
        filenameTempString = filenameTempString.replace("-", "_")
        filenameTempString = filenameTempString.replace("/", "_")
        file_name = filenameTempString + self.fileExtension


        return file_name

    def prepare(self):
        """
        准备工作
        :return:
        """
        # print(__doc__)
        print(self.name)


class PdfBook(Book):
    def makeBook(self):
        """
        make pdf book func
        :return:
        """
        print(__doc__)


class MobiBook(Book):
    def makeBook(self):
        """
        make mobi book func
        :return:
        """
        print(__doc__)


class HtmlBook(Book):
    def makeBook(self):
        """
        make html book func
        :return:
        """
        print(__doc__)


class SimpleFactory(object):
    """
    简单工厂
    """

    @staticmethod
    def createBook(bookInfo, fmt):
        """
        简单工厂
        :param bookInfo:
        :param fmt:
        :return:
        """

        if 'pdf' in fmt:
            print("create pdf factory")
            PdfBook(bookInfo, fmt)
        elif "mobi" in fmt:
            print("create mobi file")
            MobiBook(bookInfo, fmt)
        elif 'html' in fmt:
            print("create html file")
            HtmlBook(bookInfo, fmt)
        else:
            print("暂时支持pdf 和mobi和html")



print("test now")
bookInfo = BookInfo("https://flutter.cn/docs","nav_item","content")
bookCreate = SimpleFactory.createBook(bookInfo,'pdf')

