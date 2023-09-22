import os
import sys

from common.ArgsParser import ArgsParser
from common.IPChecker import check_proxy
from common.IPCrawler import IP
from workers.FateZero import FateZeroCrawler
from workers.IP3366 import IP3366Crawler
from workers.KuaiIP import KuaiIPCrawler
from workers.SeoFangFa import SeoFangFaCrawler
from workers.ZhanDaYe import ZhanDaYeCrawler


def run():
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


if __name__ == "__main__":
    run()
