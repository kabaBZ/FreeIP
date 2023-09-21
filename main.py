from workers.FateZero import FateZeroCrawler
from workers.IP3366 import IP3366Crawler
from workers.SeoFangFa import SeoFangFaCrawler
from workers.KuaiIP import KuaiIPCrawler
from workers.ZhanDaYe import ZhanDaYeCrawler
from common.IPCrawler import IP
from common.IPChecker import check_proxy

if __name__ == "__main__":
    FateZeroCrawler().main()
    IP3366Crawler().main()
    SeoFangFaCrawler().main()
    KuaiIPCrawler().main()
    ZhanDaYeCrawler().main()
    check_proxy()
