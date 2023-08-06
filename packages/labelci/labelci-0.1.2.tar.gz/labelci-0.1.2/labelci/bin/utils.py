# encoding: utf-8
# @Time: 2021/9/2 11:17 上午
# @Author: Zuo
# @File: utils.py
# @Desc:


def print_(dataset):
    """Formatted print
    """
    if isinstance(dataset, list):
        for data_info in dataset:
            print(data_info)
    else:
        print(dataset)
