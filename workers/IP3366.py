import requests
from lxml import etree
from common.IPCrawler import BaseIPCrawler, IP
from common.IPStation import IP3366


class IP3366Crawler(BaseIPCrawler):
    def __init__(self, headers=None) -> None:
        super().__init__(headers)

    # 本次更新条数
    def get_proxy_list(self):
        """
        爬取代理ip地址
        """
        ip_list = []
        params = {"stype": "1", "page": "1"}
        response = requests.get(
            IP3366.Url,
            params=params,
            headers=self.headers,
        )  # ,proxies = proxies需要时可设置代理
        print(response)
        if response.status_code == 200:
            content = response.text
            tree = etree.HTML(content)
            tr_list = tree.xpath("/html/body/div[2]/div/div[2]/table/tbody/tr")
            for tr in tr_list:
                ipv4 = tr.xpath("./td[1]/text()")[0]
                port = tr.xpath("./td[2]/text()")[0]
                ip = IP({"host": ipv4, "port": port})
                ip_list.append(ip)
        ip_list = set(ip_list)
        for ip in ip_list:
            print(ip)
        return ip_list
