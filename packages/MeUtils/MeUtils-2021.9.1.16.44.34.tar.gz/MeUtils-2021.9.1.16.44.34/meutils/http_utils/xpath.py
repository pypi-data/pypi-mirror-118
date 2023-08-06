#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : xpath
# @Time         : 2021/3/22 11:48 上午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : https://blog.csdn.net/u013332124/article/details/80621638
# pd: https://blog.csdn.net/zhang862520682/article/details/86701078


from lxml.etree import HTML
from meutils.http_utils import request

# r = request(parser=None)
# dom_tree = HTML(r.text)
# dom_tree.xpath('//*[@id="sogou_vr_11002601_box_0"]/div[2]')


def get_dom_tree(url, xpath="""//*[@id="a_ft_1"]//text()"""):
    r = request(url, parser=None)
    dom_tree = HTML(r.text)
    return dom_tree.xpath(xpath)


if __name__ == '__main__':
    _ = get_dom_tree(
        "http://www.pkulaw.cn/cluster_form.aspx?Db=news&menu_item=law&EncodingName=&keyword=&range=name&",
        """//*[@id]//@href"""

    )
    print(_)
