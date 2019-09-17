# from django.test import TestCase
#
#
# # Create your tests here.
# import re
# import urllib.request as request
# from bs4 import BeautifulSoup
# import requests
#
# '''全局变量声明， 下载其它小说请注意修改 [下载到的本地目录, 书号, 起始index号]'''
# downLoadFile = r'D:\bbstest1\static'  ##要下载到的目录
# shuhao = '11_11850'  ## 书号就是http://www.biquge.com/2_2970/2456497.html; com后面的那个。
# start, end = 7635421, 10
#
#
# def setSrr(url):
#     if (requests.get(url).status_code == 404):
#         print('这是个错误网址')
#         return []
#     print('正在打开 ', url)
#
#     l = []
#     '''''请求响应和不响应的处理'''
#     response = request.urlopen(url)
#
#     html = response.read().decode('GBK')
#     print(html)
#     soup = BeautifulSoup(html)
#     item = str(soup.findAll('h1')[0])
#     title = item[5:-6]
#     l.append(title.split(' ')[0])
#     l.append(title)
#     strings = soup.findAll('div', id="content")[0]
#     for string in strings:
#         st = string.__str__()
#         if (len(st.split('<br/>')) > 1):
#             pass
#         else:
#             l.append(st)
#     return l
#
#
# # strings.split()
#
# # 穿入字符串 写入文件；标题为l[0]
# def setDoc(l):
#     if (len(l) < 2):
#         return
#     file_s = downLoadFile + l[0] + '.txt'
#     file = open(file_s, 'w+', encoding='utf-8')
#     for i in l:
#         file.write('\t')
#         for ii in i.split('    '):
#             file.write(ii)
#         file.write('\n')
#
#     # 开始自加数值；读取新文档；如果没有；那么跳过
#
#
# ''''' 最开始设置为1066142，100  '''
#
#
# def setNum(num, n):
#     l = [(num + i) for i in range(n)]
#     sl = [str(l[i]) for i in range(len(l))]
#     return sl
#
#
# '''''自动产生新的url'''
#
# '''''  自己观察到： 第一章的地址http://www.biquge.com/2_2970/2456497.html
# 最后一张的地址 http://www.biquge.com/2_2970/3230837.html'''
#
#
# def setNewUrl(sl):
#     urls = []
#     for x in sl:
#         xsr = 'http://www.biquge.com.tw/' + shuhao + '/' + x + '.html'  # 对应的单章html
#         urls.append(xsr)
#     return urls
#
#
# def setTxts(urls):
#     for url in urls:
#         setDoc(setSrr(url))
#
#
# print(
#     '''''
#     --------------
#     开始下载超品相师
#     --------------
#     ——actanble 手打——
#     如果要下载其他的txt文件: 请修改——
#     URL 和 对应的起始html的index号。
#     '''
# )
# setTxts(setNewUrl(setNum(start, end)))

#
# # !/usr/bin/env Python
# # coding=utf-8
# import time
# import urllib.request
# import re
# from bs4 import BeautifulSoup
#
#
# def open_url(url):
#     req = urllib.request.Request(url)
#     req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0')
#     response = urllib.request.urlopen(req)
#     html = response.read().decode('gbk')  # gbk格式的
#     return html
#
#
# def search_novel():  # 实现查找到小说，并且返回该小说所在笔趣阁网页的代码
#     content = input('请输入你想要查找的小说名：')
#     initial_content = content
#     content += ' site:biquge5.com'
#     content_code = urllib.request.quote(content)  # 解决中文编码的问题
#
#     url = 'https://www.baidu.com/s?wd=' + content_code
#
#     req = urllib.request.Request(url)
#     req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0')
#     response = urllib.request.urlopen(req)
#
#     html = response.read().decode('utf-8')
#
#     link_list = re.findall(r'<div class.*?c-container[\s\S]*?href[\s\S]*?http://([\s\S]*?)"', html)
#
#     for url in link_list:
#         url = 'http://' + url
#
#         req = urllib.request.Request(url)
#         req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0')
#         response = urllib.request.urlopen(req)
#
#         real_url = response.geturl()
#         print('小说《' + initial_content + '》笔趣阁在线阅读地址是：' + real_url)
#         return real_url
#
#
# def get_title(html):
#     '获取该URL页面小说的章节标题'
#     p = r'<h1>(.*?)</h1>'
#     title = re.findall(p, html)  # 加上()直接返回括号内的内容
#     print(title[0])
#     return title[0]
#
#
# def get_content(html):
#     '获取该URL页面的小说内容'
#     p = r'<div id="content">([\s\S]*?)</div>'  # ？启用非贪婪模式
#     content = re.findall(p, html)
#
#     content[0] = content[0].replace(' ', ' ')
#     content[0] = content[0].replace('<br />', '')
#     content = re.sub(r'<a.*?>(.*?)</a>', '', content[0])  # 去除里面的<a>元素
#     return content
#
#
# def write_into_file(title, content):
#     '将标题和内容写入文件'
#     f = open('C:\\Users\\Administrator\\Desktop\\fiction.txt', 'a')
#     f.writelines(title + '\n\n')
#     f.writelines(content + '\n\n')
#     f.close()
#
#
# def get_every_page_url(content):
#     '得到每页的URL'
#     soup = BeautifulSoup(content,content.parser)
#     link_list = soup.find_all('ul','._chapter')
#     print(link_list)
#     exit()
#     return link_list
#
#
# if __name__ == '__main__':
#     url = search_novel()
#     content = open_url(url)
#
#     link_list = get_every_page_url(content)
#
#     for url in link_list:
#         url = 'http://www.guibuyu.org' + url
#         html = open_url(url)
#         time.sleep(5)  # 为了防止网站反爬，就sleep了一下。
#         write_into_file(get_title(html), get_content(html))


# import re
# import os
# import sys
# from bs4 import BeautifulSoup
# from urllib import request
# import ssl
# url = 'http://www.biqiuge.com/book/4772/'
# # url = 'https://www.qu.la/book/1/'
# # url = 'http://www.biqiuge.com/book/1/'
#
# def getHtmlCode(url):
#     page = request.urlopen(url)
#     html = page.read()
#     htmlTree = BeautifulSoup(html,'html.parser')
#     return htmlTree
#     #return htmlTree.prettify()
# def getKeyContent(url):
#     htmlTree = getHtmlCode(url)
#
# def parserCaption(url):
#     htmlTree = getHtmlCode(url)
#     storyName = htmlTree.h2.get_text() + '.txt'
#
#     aList = htmlTree.find_all('a',href=re.compile('(\d)*.html'))  #aList是一个标签类型的列表，class = Tag 写入文件之前需要转化为str
#     aList = set(aList)
#
#     aDealList = []
#     for line in aList:
#         chapter = int(line['href'].strip().split('/')[3].strip('.html'))
#         aDealList.append(chapter)
#     aDealList.sort()    #排序
#     urlList = []
#     for line in aDealList:
#         line = url + str(line) + '.html'
#         urlList.append(line)
#     # print(urlList)
#     print(urlList)
#     return (storyName,urlList)
# def parserChapter(url):
#     htmlTree = getHtmlCode(url)
#     print(htmlTree)
#     title = htmlTree.h1.get_text()  #章节名
#     content = htmlTree.find_all('div',id = 'content')
#     content = content[0].contents[1].get_text()
#     print(content)
#     return (title,content)
# def main(url):
#     (storyName,urlList) = parserCaption(url)
#     flag = True
#     cmd = 'del ' + storyName
#     os.system(cmd)
#     cmd = 'cls'
#     count = 1
#     for url_alone in urlList:
#         percent = count / len(urlList) * 100
#         print('%s 下载进度 %0.2f %%'%(storyName,percent))
#         f = open(storyName,'a+',encoding = 'utf-8')
#         (title,content) = parserChapter(url_alone)
#         tmp = title + '\n' + content
#         f.write(tmp)
#         f.close()
#         count = count + 1
#
# main(url)
# def Singleton(cls):
#     _instance = {}
#
#     def _singleton(*args, **kargs):
#         if cls not in _instance:
#             _instance[cls] = cls(*args, **kargs)
#         return _instance[cls]
#
#     return _singleton
#
#
# @Singleton
# class A(object):
#     a = 1
#
#     def __init__(self, x=0):
#         self.x = x
#
#
# a1 = A(2)
# a2 = A(3)
# print(id(a1), id(a2))
# print(a1.x, a2.x)

#
# class SingletonType(type):
#     def __init__(self, *args, **kwargs):
#         print('Singleinit')
#         super(SingletonType, self).__init__(*args, **kwargs)
#
#     def __call__(cls, *args, **kwargs):  # 这里的cls，即Foo类
#         print('cls', cls)
#         obj = cls.__new__(cls, *args, **kwargs)
#         cls.__init__(obj, *args, **kwargs)  # Foo.__init__(obj)
#         return obj
#
#
# class Foo(metaclass=SingletonType):  # 指定创建Foo的type为SingletonType
#     def __init__(self, name):
#         self.name = name
#         print(name,'name')
#
#     def __new__(cls, *args, **kwargs):
#         print('foonew')
#         return object.__new__(cls)
#
#
# obj = Foo('xx')
print(1<2==2)
print(2<3==3)
print(1<2<3<4>5)
