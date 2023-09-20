import requests

XT_Token = "dpkkUtf7euD4GRM7kqrWJegNS"


class XiaTuiAlert(object):
    def send(title, msg=""):
        mydata = {"text": title, "desp": msg}

        requests.post(f"http://wx.xtuis.cn/{XT_Token}.send", data=mydata)
