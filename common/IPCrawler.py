import json
import traceback
from abc import abstractmethod

import requests
from common.AlertUtils import XiaTuiAlert
from common.DBUtils import RedisOpration, RedisProfile
from requests.exceptions import ProxyError, Timeout


class IP(object):
    def __init__(self, ip_dict: dict) -> dict:
        self.ip_info = ip_dict
        self.host = ip_dict.get("host")
        self.port = ip_dict.get("port")
        self.user = ip_dict.get("user")
        self.pw = ip_dict.get("pw")
        if self.user and self.pw:
            proxy_str = f"{self.user}:{self.pw}@{self.host}:{self.port}"
        else:
            proxy_str = f"{self.host}:{self.port}"
        self.proxy = {"http": f"http://{proxy_str}", "https": f"https://{proxy_str}"}
        if any([not self.host, not self.port]):
            self.proxy = {}

    def update_ip_info(self, info: dict):
        if info.get("timestamp"):
            del info["timestamp"]
        self.ip_info.update(info)

    def __str__(self) -> str:
        return json.dumps(self.ip_info, ensure_ascii=False)

    def __repr__(self) -> str:
        return json.dumps(self.ip_info, ensure_ascii=False)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, IP):
            return False
        return self.proxy == __value.proxy

    def __hash__(self):
        return hash(json.dumps(self.proxy, ensure_ascii=False))


class IvalidProxyException(Exception):
    def __init__(self) -> None:
        self.message = "Invalid proxy!"

    def __str__(self) -> str:
        return self.message


class IvalidAuthException(Exception):
    def __init__(self) -> None:
        self.message = "Invalid auth params, asking for keys: <user>/<pw>!"

    def __str__(self) -> str:
        return self.message


class IpTestException(Exception):
    def __init__(self) -> None:
        self.message = "Abnormal Status Code"

    def __str__(self) -> str:
        return self.message


class BaseIPCrawler(object):
    Test_url = "http://myip.top/"

    def __init__(self, headers=None) -> None:
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        }

    def test_ip(self, ip: IP, test_url: str = None) -> bool:
        try:
            res = requests.get(
                test_url or self.Test_url,
                headers=self.headers,
                proxies=ip.proxy,
                timeout=2,
                verify=False,
            )
            if res.status_code != 200:
                raise IpTestException
            try:
                ip_info = res.json()
            except Exception as e:
                print("res.json()报错：{}".format(res.text))
                raise e
            ip.update_ip_info(ip_info)
            print(ip)
            return True
        except (Timeout, ProxyError):
            print("代理验证失败：{}".format(ip))
            return False
        except IpTestException:
            print("验证URL响应报错{}:{}".format(ip, res.status_code))
            return False
        except Exception as E:
            print("代理请求构筑失败：{}".format(ip))
            print(traceback.format_exc())
            return False

    @abstractmethod
    def save_to_db(self) -> None:
        pass

    @abstractmethod
    def get_proxy_list(self) -> set:
        pass

    def main(self):
        self.ip_list = self.get_proxy_list()
        updated_proxy = []
        msg = ""
        for ip in self.ip_list:
            if self.test_ip(ip):
                updated_proxy.append(ip)
                msg += f"<br>{str(ip)}"
                RedisOpration(RedisProfile).sadd(
                    "proxy_test", json.dumps(ip.ip_info, ensure_ascii=False)
                )
                continue
                # todo
                self.save_to_db(ip)

        XiaTuiAlert.send(
            title=f"本次{self.__class__.__name__}任务共更新{len(updated_proxy)}条数据", msg=msg
        )


if __name__ == "__main__":
    BaseIPCrawler().main()
