import requests
import os


class XiaTuiAlert(object):
    def send(title, msg=""):
        XT_Token = os.environ.get("XT_Token")
        if not XT_Token:
            print("系统变量中不存在虾推Token!")
        mydata = {"text": title, "desp": msg}

        requests.post(f"http://wx.xtuis.cn/{XT_Token}.send", data=mydata)
