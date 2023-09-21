from workers.FateZero import FateZeroCrawler
from workers.IP3366 import IP3366Crawler
from workers.SeoFangFa import SeoFangFaCrawler
from workers.KuaiIP import KuaiIPCrawler
from workers.ZhanDaYe import ZhanDaYeCrawler
from common.IPCrawler import IP
from common.IPChecker import check_proxy
from common.ArgsParser import ArgsParser
import sys
import os

if __name__ == "__main__":
    token = ArgsParser(sys.argv[1:])
    if token:
        os.environ["XT_Token"] = token
    else:
        XT_Token = os.environ.get("XT_Token")
        if not XT_Token:
            raise Exception("系统变量中不存在虾推Token!")

    FateZeroCrawler().main()
    IP3366Crawler().main()
    SeoFangFaCrawler().main()
    KuaiIPCrawler().main()
    ZhanDaYeCrawler().main()
    check_proxy()
