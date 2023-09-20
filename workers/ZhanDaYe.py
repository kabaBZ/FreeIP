import copy
import time
from redis import Redis
import requests
from lxml import etree
import random
from copy import deepcopy
from common.IPCrawler import IP, BaseIPCrawler
from common.IPStation import ZhanDaYe
import datetime


class ZhanDaYeCrawler(BaseIPCrawler):
    def __init__(self, headers=None) -> None:
        super().__init__(headers)
        self.headers.update({"Host": "www.zdaye.com"})
        self.host = "https://www.zdaye.com"
        self.detail_url = []

    def get_detail_url_list(self):
        today = datetime.datetime.now()
        self.headers.update({"Referer": ZhanDaYe.Url.format(today.year, today.month)})
        res = requests.get(
            ZhanDaYe.Url.format(today.year, today.month), headers=self.headers
        )
        if res.status_code == 200:
            res.encoding = "utf-8"
            home_page = etree.HTML(res.text)
            cn_date = f"{today.month}月{today.day}日"
            cn_date2 = f"{today.month}月{today.day - 1}日"
            detail_url_list = home_page.xpath(
                f"//a[contains(text(), '{cn_date}')]/@href"
            )
            detail_url_list2 = home_page.xpath(
                f"//a[contains(text(), '{cn_date2}')]/@href"
            )
            self.detail_url.extend(detail_url_list)
            self.detail_url.extend(detail_url_list2)

    def get_proxy_list(self):
        self.get_detail_url_list()
        proxy_list = []
        for url in self.detail_url:
            next = True
            page = 1
            while next:
                # 防风控
                time.sleep(5)
                req_url = self.host + url.replace(".html", f"/{page}.html")
                res = requests.get(req_url, headers=self.headers)
                res.encoding = "utf-8"
                if res.status_code == 200:
                    detail_page = etree.HTML(res.text)
                    trs = detail_page.xpath("//tbody//tr")
                    for tr in trs:
                        proxy = IP(
                            {
                                "host": tr.xpath("./td[1]/text()")[0],
                                "port": tr.xpath("./td[2]/text()")[0],
                            }
                        )
                        proxy_list.append(proxy)
                    if not detail_page.xpath('//a[@title="下一页"]'):
                        next = False
                else:
                    break
        proxy_list = set(proxy_list)
        for ip in proxy_list:
            print(ip)
        return proxy_list
