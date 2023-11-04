import json
import datetime
import traceback
import requests
import asyncio
import time

import aiohttp
from aiohttp.client_exceptions import ServerTimeoutError, ClientHttpProxyError
from aiohttp import ClientSession

from requests.exceptions import ProxyError, Timeout
from FreeIP.common.IPCrawler import IP, BaseIPCrawler, IpTestException
from FreeIP.Utils.AlertUtils import XiaTuiAlert
from FreeIP.Utils.DBUtils import RedisOpration, RedisProfile


redis_db = RedisOpration(RedisProfile)


async def test_ip_async(ip: IP, test_url: str = None) -> bool:
    try:
        proxy = ip.proxy['http']
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        }
        async with ClientSession(connector=aiohttp.TCPConnector(ssl=False), trust_env=True, timeout=10) as session:
            async with session.get(
                test_url,
                proxy=proxy,
                timeout=20,
                headers=headers,
                verify_ssl=False,
            ) as response:
                ip_info = await response.json()
                if response.status != 200:
                    raise IpTestException
                try:
                    ip.update_ip_info(ip_info)
                except Exception as e:
                    print("res.json()报错：{}".format(response.text()))
                    raise e
                print(ip)
                return True
    except (ServerTimeoutError, ):
        print("代理验证失败：{}".format(ip))
        return False
    except ClientHttpProxyError:
        # print(traceback.format_exc())
        print("代理设置失败：{}".format(ip))
        return True
    except IpTestException:
        print("验证URL响应报错{}:{}".format(ip, response.status))
        return False
    except Exception as E:
        print("代理请求构筑失败：{}".format(ip))
        print(traceback.format_exc())
        return False


async def check_proxy_async(proxy, url):
    ip = IP(proxy)
    if not await test_ip_async(ip, url):
        if redis_db.srem("proxy_test", proxy):
            print(f'db删除成功{proxy}')
            return False, True
        else:
            print(f'db删除失败{proxy}')
            return False, False
    else:
        return True, True


def check_proxy_sync():

    proxy_list = redis_db.smembers("proxy_test")

    removed_count = 0
    remove_failed_count = 0
    for proxy in proxy_list:
        ip = IP(proxy)
        if not BaseIPCrawler().test_ip(ip):
            if redis_db.srem("proxy_test", proxy):
                removed_count += 1
            else:
                remove_failed_count += 1
    proxy_num = redis_db.scard("proxy_test")
    XiaTuiAlert.send(
        title="代理复核任务完成",
        msg=f"失效代理{removed_count + remove_failed_count}个：<br>成功移除{removed_count}个，失败{remove_failed_count}个！<br>数据库中剩余代理数量：{proxy_num}!",
    )


async def main():
    url = "https://myip.top/"
    task_list = []
    db_proxys = redis_db.smembers("proxy_test")

    for proxy in db_proxys:
        task = asyncio.ensure_future(check_proxy_async(proxy, url))
        task_list.append(task)
    done, pending = await asyncio.wait(task_list, timeout=None)
    removed_count = 0
    remove_failed_count = 0
    # 得到执行结果
    for done_task in done:
        if done_task.result()[0]:
            continue
        if not done_task.result()[1]:
            remove_failed_count += 1
        else:
            removed_count += 1
    proxy_num = redis_db.scard("proxy_test")
    XiaTuiAlert.send(
        title="代理复核任务完成",
        msg=f"失效代理{removed_count + remove_failed_count}个：<br>成功移除{removed_count}个，失败{remove_failed_count}个！<br>数据库中剩余代理数量：{proxy_num}!",
    )


def check_proxy(use_async=True):
    start = time.time()
    if use_async:
        check_proxy_sync()
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    print(f'总时间：{time.time() - start}')


if __name__ == "__main__":
    check_proxy()
