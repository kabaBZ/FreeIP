#!/usr/bin/python
# -*- coding: UTF-8 -*-


import sys
import getopt


def ArgsParser(argv):
    """
    通过 getopt模块 来识别参数demo,  http://blog.csdn.net/ouyang_peng/
    """

    XT_Token = ""

    try:
        """
        options, args = getopt.getopt(args, shortopts, longopts=[])

        参数args：一般是sys.argv[1:]。过滤掉sys.argv[0]，它是执行脚本的名字，不算做命令行参数。
        参数shortopts：短格式分析串。例如："hp:i:"，h后面没有冒号，表示后面不带参数；p和i后面带有冒号，表示后面带参数。
        参数longopts：长格式分析串列表。例如：["help", "ip=", "port="]，help后面没有等号，表示后面不带参数；ip和port后面带冒号，表示后面带参数。

        返回值options是以元组为元素的列表，每个元组的形式为：(选项串, 附加参数)，如：('-i', '192.168.0.1')
        返回值args是个列表，其中的元素是那些不含'-'或'--'的参数。
        """
        opts, args = getopt.getopt(argv, "ht:", ["help", "XT_Token="])
    except getopt.GetoptError:
        print("Error: -t <XT_Token>")
        print("   or: --XT_Token=<XT_Token>")
        sys.exit(2)

    # 处理 返回值options是以元组为元素的列表。
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(" -t <XT_Token>")
            print("or: --XT_Token=<XT_Token>")
            sys.exit()
        elif opt in ("-t", "--XT_Token"):
            XT_Token = arg
    print("XT_Token为:", XT_Token)
    return XT_Token


if __name__ == "__main__":
    # sys.argv[1:]为要处理的参数列表，sys.argv[0]为脚本名，所以用sys.argv[1:]过滤掉脚本名。
    ArgsParser(sys.argv[1:])
