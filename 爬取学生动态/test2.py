#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：spider_demo 
@File    ：test2.py
@IDE     ：PyCharm 
@Author  ：liyuda
@Date    ：2024/11/5 22:02 
'''
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 定义基本URL和要保存的目录
base_url = "http://ibschool.hnu.edu.cn/website2022wz/xsfz/xsdt.htm"
save_directory = "dynamic"

# 创建保存目录
os.makedirs(save_directory, exist_ok=True)

def fetch_page(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_and_save(html, page_number):
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.select(".article-list a")  # 修改选择器以匹配实际网站结构
    for article in articles:
        article_url = urljoin(base_url, article['href'])
        article_html = fetch_page(article_url)
        article_soup = BeautifulSoup(article_html, 'html.parser')
        print(article_soup)

        # 保存文章到本地
        article_title = article_soup.title.string.strip()
        filename = f"page_{page_number}_{article_title}.html"
        filepath = os.path.join(save_directory, filename)

        with open(filepath, 'w', encoding='utf-8') as file:
            # 修正图片和链接路径
            for img in article_soup.find_all('img'):
                img['src'] = urljoin(article_url, img['src'])
            for link in article_soup.find_all('a'):
                link['href'] = urljoin(article_url, link['href'])
            file.write(str(article_soup))

def main():
    for page_number in range(1, 4):  # 爬取前3页
        page_url = f"http://ibschool.hnu.edu.cn/website2022wz/xsfz/xsdt/{page_number}.htm"
        page_html = fetch_page(page_url)
        # print(page_html)
        parse_and_save(page_html, page_number)

if __name__ == "__main__":
    main()