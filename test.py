import json

import requests

from common.IPCrawler import IP, BaseIPCrawler
from Utils.DBUtils import RedisOpration, RedisProfile

if __name__ == "__main__":
    # print(
    #     BaseIPCrawler().test_ip(
    #         IP({"host": "45.167.125.61", "port": "9992"}),
    #         test_url="http://httpbin.org/ip",
    #     )
    # )

    ip = IP({"host": "110.110.110.1", "port": "1110"})
    RedisOpration(RedisProfile).sadd(
        "proxy_test", json.dumps(ip.ip_info, ensure_ascii=False)
    )
