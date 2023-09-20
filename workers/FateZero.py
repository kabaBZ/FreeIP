import requests
from common.IPCrawler import BaseIPCrawler, IP
from common.IPStation import FateZero
import json


class FateZeroCrawler(BaseIPCrawler):
    def __init__(self, headers=None) -> None:
        super().__init__(headers)
        self.headers.update({"Referer": "http://www.ip3366.net/free/"})

    # 本次更新条数
    def get_proxy_list(self):
        """
        爬取代理ip地址
        """
        ip_list = []
        url = FateZero.Url
        response = requests.get(
            url,
            headers=self.headers,
        )  # ,proxies = proxies需要时可设置代理
        dic_list = response.text.split("\n")
        for item in dic_list:
            if not item.strip():
                continue
            item = json.loads(item)
            temp_ = IP(
                {
                    "host": item["host"],
                    "port": item["port"],
                    "user": item.get("username"),
                    "pw": item.get("pw"),
                }
            )
            ip_list.append(temp_)
        ip_list = set(ip_list)
        for ip in ip_list:
            print(ip)
        return ip_list


if __name__ == "__main__":
    FateZeroCrawler().main()
