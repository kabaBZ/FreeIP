import requests
import os

XT_Token = os.environ.get("XT_Token")
if not XT_Token:
    raise Exception("系统变量中不存在虾推Token!")


class XiaTuiAlert(object):
    def send(title, msg=""):
        mydata = {"text": title, "desp": msg}

        requests.post(f"http://wx.xtuis.cn/{XT_Token}.send", data=mydata)
