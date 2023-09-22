import copy

import requests
from common.IPCrawler import IP, BaseIPCrawler
from common.IPStation import SeoFangFa
from lxml import etree


class SeoFangFaCrawler(BaseIPCrawler):
    def __init__(self, headers=None) -> None:
        super().__init__(headers)

    def get_proxy_list(self):
        """
        爬取代理ip地址
        """
        ip_list = []
        response = requests.get(
            SeoFangFa.Url,
            headers=self.headers,
        )  # ,proxies = proxies需要时可设置代理
        tree = etree.HTML(response.text)
        tr_list = tree.xpath("//tbody/tr")
        for tr in tr_list:
            ipv4 = tr.xpath("./td[1]/text()")[0]
            port = tr.xpath("./td[2]/text()")[0]
            ip = ipv4 + ":" + port
            ip = IP({"host": ipv4, "port": port})
            ip_list.append(ip)
        ip_list = set(ip_list)
        for ip in ip_list:
            print(ip)
        return ip_list
