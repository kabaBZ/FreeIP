import random
import requests
from lxml import etree
from common.IPCrawler import IP, BaseIPCrawler
from common.IPStation import KuaiIP
import random


class KuaiIPCrawler(BaseIPCrawler):
    def __init__(self, headers=None) -> None:
        super().__init__(headers)

    def get_proxy_list(self):
        """
        爬取代理ip地址
        """
        ip_list = []
        response = requests.get(
            KuaiIP.Url,
            headers=self.headers,
        )  # ,proxies = proxies需要时可设置代理
        if response.status_code == 200:
            content = response.text
            tree = etree.HTML(content)
            tr_list = tree.xpath("//tbody/tr")
            for tr in tr_list:
                ipv4 = tr.xpath("./td[1]/text()")[0]
                port = tr.xpath("./td[2]/text()")[0]
                ip = IP({"host": ipv4, "port": port})
                ip_list.append(ip)
        ip_list = set(ip_list)
        for ip in ip_list:
            print(ip)
        return ip_list
