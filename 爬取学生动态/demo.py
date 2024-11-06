#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：spider_demo 
@File    ：demo.py
@IDE     ：PyCharm 
@Author  ：liyuda
@Date    ：2024/11/5 21:19 
'''
import datetime

import requests
from lxml import etree
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
now = datetime.datetime.now()
formatted_time = now.strftime('%Y-%m-%d_%H.%M.%S')
class spider_project:
    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-GB,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "JSESSIONID=1597E3769073C18658976C9E4AC6A073",
            "Pragma": "no-cache^",
            "Upgrade-Insecure-Requests": "1^",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
        }
        job_path = Path(f"./Downloads/{formatted_time}/学生动态首页")
        job_path_2 = Path(f"./Downloads/{formatted_time}/学生动态详情")
        job_path.mkdir(parents=True)
        job_path_2.mkdir(parents=True)


    def get_data(self,parmas):
        url = f"http://ibschool.hnu.edu.cn/website2022wz/xsfz/xsdt/{parmas}.htm"
        response = requests.get(url, headers=self.headers)
        response.encoding = 'utf-8'
        return response.text

    def save_data(self,res,filename):
        with open(filename,"w",encoding="utf-8") as f:
            f.write(res)
        print(f"保存成功{filename}")

    def save_info_data(self,res):
        html = etree.HTML(res)
        info_list = html.xpath('//div[@class="cover"]/a/@href')
        for info in info_list:
            url_info=info.split('/')
            if len(url_info)==6:
                url=f"http://ibschool.hnu.edu.cn/info/{url_info[4]}/{url_info[5]}"
                res = requests.get(url, headers=self.headers)
                res.encoding = 'utf-8'
                base_url = f"http://ibschool.hnu.edu.cn"
                soup= BeautifulSoup(res.text,"html.parser")
                for img in soup.find_all('img'):
                    if img.has_attr('src'):
                        img['src']=urljoin(base_url,img['src'])
                    if img.has_attr('orisrc'):
                        img['orisrc']=urljoin(base_url,img['orisrc'])
                    if img.has_attr('vurl'):
                        img['vurl']=urljoin(base_url,img['vurl'])
                modified_html = str(soup)
                self.save_data(modified_html,f"./Downloads/{formatted_time}/学生动态详情/{url_info[5]}")



    def main(self):
        for url_obj in range(1,16):
            res=self.get_data(url_obj)
            self.save_data(res,f'./Downloads/{formatted_time}/学生动态首页/{url_obj}.html')
            self.save_info_data(res)


if __name__ == '__main__':
    spider = spider_project()
    spider.main()


