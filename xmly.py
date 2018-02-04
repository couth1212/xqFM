#!/usr/bin/python3
# -*- coding:utf-8 -*-
#----------------------------------------
#文件: xmly.py
#作者: String
#邮箱: 18093329352@163.com
#时间: 2018年02月02日 星期五 18时35分29秒
#----------------------------------------

import requests
import re
import random

# 获得网页源码
def getHtml(url_cate):
    s = requests.Session()
    # 身份列表
    user = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 UBrowser/5.6.13705.206 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36']
    # 身份构建
    headers = {'User-Agent':random.choice(user)}
    html = s.get(url=url_cate, headers=headers, timeout=20).text
    return html
        
# 分析分类页URL
def getTypeUrl(html):
    # 分类列表
    re_urls = r'<ul data-reactid="32">(.*?)</ul>'
    # 分类列表html
    url_urls = re.findall(re_urls, html, re.S|re.M)[0]
    # 分类正则
    re_type = r'<a class=".*?" href="(.*?)" data-reactid=".*?">(.*?)</a>'
    # 分类网址
    url_type = re.findall(re_type, url_urls)
    # 对结果进行整理 li列表用来存储整理结果
    li = []
    for x in url_type:
        href = 'http://www.qingting.fm' + x[0][:-1]
        name = x[1]
        li.append((name, href))
    return li

# 获取内容页内容URL
def getPageUrl(href_ip, filename):
    page_url = getHtml(href_ip)
    re_page = r'<a class="nVFQ" href="(.*?)" data-reactid=".*?">'
    page = re.findall(re_page, page_url, re.S|re.M)
    for x in page:
        temp = 'http://www.qingting.fm' + x
        getContent(temp)


# 获取内容
def getContent(temp):
    print(temp)
    html = getHtml(temp)
    # 获得含有有效信息的HTML
    re_tag = r'<div class="_33eu _2lyJ" (.*?)</div></div>'
    tag = re.findall(re_tag, html, re.S|re.M)[0]
    # 标题
    tag_title = r'<h1 class="_3h7q" data-reactid="43">(.*?)</h1>'
    title = re.findall(tag_title, tag)[0]
    # 访问量
    tag_inq = r'</span><span class="_8-O6" data-reactid=".*?"><!-- react-text: .*? -->(.*?)<!-- /react-text -->'
    inq = re.findall(tag_inq, tag)[0]
    # 最近更新
    tag_update = r'<span class="_1Hqd" data-reactid=".*?">最近更新：</span><span data-reactid=".*?">(.*?)</span>'
    update = re.findall(tag_update, tag)[0]
    # 主播Anchor
    tag_anchor = r'<span class="_1Hqd" data-reactid=".*?">主播：</span><span data-reactid=".*?"><img class=".*?" src=".*?" alt=".*?" data-reactid=".*?"/></span><span data-reactid=".*?">(.*?)</span>'
    anchor = re.findall(tag_anchor, tag)
    if anchor == []:
        anchor = '无'
    else:
        anchor = anchor[0]
    li = [title, inq, update, anchor]
    print(title, inq, update, anchor)
    return li

if __name__ == '__main__':
    # 分类页网址
    url_cate = 'http://www.qingting.fm/categories'
    html = getHtml(url_cate)
    li = getTypeUrl(html)

    lt = []
    for i in range(2, len(li)):
        lt.append(li[i])

    for x in lt:
        print(x)
        for t in range(1, 3):
            href_ip = x[1] + str(t)
            getPageUrl(href_ip, x[0])

    # url = 'http://www.qingting.fm/channels/238946'
    # print(getContent(url))