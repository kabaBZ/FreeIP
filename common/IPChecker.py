import json

from common.AlertUtils import XiaTuiAlert
from common.DBUtils import RedisOpration, RedisProfile
from common.IPCrawler import IP, BaseIPCrawler


def check_proxy():
    redis = RedisOpration(RedisProfile)
    proxy_list = redis.smembers("proxy_test")

    removed_count = 0
    remove_failed_count = 0
    for proxy in proxy_list:
        ip = IP(proxy)
        if not BaseIPCrawler().test_ip(ip):
            if redis.srem("proxy_test", proxy):
                removed_count += 1
            else:
                remove_failed_count += 1
    proxy_num = redis.scard("proxy_test")
    XiaTuiAlert.send(
        title="代理复核任务完成",
        msg=f"失效代理{removed_count + remove_failed_count}个：<br>成功移除{removed_count}个，失败{remove_failed_count}个！<br>数据库中剩余代理数量：{proxy_num}!",
    )
