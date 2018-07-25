from bs4 import BeautifulSoup
import subprocess as sp
from lxml import etree
import requests
import random
import re


def get_proxys(page=1):
    list={'1': 'http://www.xicidaili.com/nt/', # xicidaili国内普通代理
          '2': 'http://www.xicidaili.com/nn/', # xicidaili国内高匿代理
          '3': 'http://www.xicidaili.com/wn/', # xicidaili国内https代理
          '4': 'http://www.xicidaili.com/wt/'} # xicidaili国外http代理
    S = requests.Session()
    proxys_list = []
    while page > 0:
        for type in [1,2,3,4]:
            target_url = list[str(type)] + str(page)
            target_headers = {'Upgrade-Insecure-Requests': '1',
                              'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                              'Referer': 'http://www.xicidaili.com/nn/',
                              'Accept-Encoding': 'gzip, deflate, sdch',
                              'Accept-Language': 'zh-CN,zh;q=0.8',
                              }
            target_response = S.get(url=target_url, headers=target_headers)
            target_response.encoding = 'utf8'
            target_html = target_response.text
            bf1_ip_list = BeautifulSoup(target_html, 'lxml')
            bf2_ip_list = BeautifulSoup(str(bf1_ip_list.find_all(id='ip_list')), 'lxml')
            # 提取bf2_ip_list中的table元素,并返回列表 bs.contents返回列表
            ip_list_info = bf2_ip_list.table.contents
            for index in range(len(ip_list_info)):
                if index % 2 == 1 and index != 1:
                    dom = etree.HTML(str(ip_list_info[index]))
                    ip = dom.xpath('//td[2]')
                    port = dom.xpath('//td[3]')
                    protocol = dom.xpath('//td[6]')
                    ip = ip[0].text + ':' + port[0].text
                    proxy = protocol[0].text.lower() + "://" + ip
                    if check_ip('http://www.xicidaili.com', proxy):
                        print(proxy+"可用")
                        proxys_list.append(ip)
        page -= 1
    return proxys_list

def check_ip(url, ip):
    headers = {'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Referer': 'http://www.xicidaili.com/nn/',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               }
    proxies = {"http" : ip, "https" : ip}
    try:
        response = requests.get(url=url, proxies=proxies, headers=headers, timeout=2).status_code
        if response == 200:
            return True
        else:
            return False
    except:
        return False


if __name__ == '__main__':
    proxys_list = get_proxys(1)
    for ip in proxys_list:
        print(ip)