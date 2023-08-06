#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : wecom
# @Time         : 2021/8/31 下午5:16
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : https://github.com/quanttide/wecom-sdk-py/tree/master/wechatwork_sdk


from meutils.pipe import *
from meutils.hash_utils import *


class Text(BaseConfig):
    content = ""


class Article(BaseConfig):
    title: str = '百度热榜'
    description: str = '百度热榜'
    url: str = 'https://top.baidu.com/board?tab=realtime'
    picurl: str = 'http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png'


test_hook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=1eb25317-39a1-4af7-a6e3-63877ec2dd64"


class Bot(object):

    def __init__(self, hook_url='1eb25317-39a1-4af7-a6e3-63877ec2dd64'):
        self.hook_url = self._convert_hook_url(hook_url)

    def send(self, body=None):
        if body is None:
            body = {
                "msgtype": "text",
                "text": {
                    "content": "南京今日天气：29度，大部分多云，降雨概率：60%",
                    "mentioned_mobile_list": ["18550288233", "@all"]
                }
            }
        return requests.post(url=self.hook_url, json=body)

    def send_text(self, ):
        msgtype = self.__name__.split("_")[1]

        json = {
            "msgtype": msgtype,
            msgtype: {}
        }

    def send_news_(self, articles: Union[Article, List[Article]]):
        json = {
            "msgtype": "news",
            "news": {
                "articles": []
            }
        }
        if isinstance(articles, Article):
            articles = [articles]

        for article in articles:
            json["news"]["articles"].append(article.dict())
        self.send(json)

    def send_news(self):
        json = {
            "msgtype": "news",
            "news": {
                "articles": [
                    {
                        "title": "中秋节礼品领取1",
                        "description": "今年中秋节公司有豪礼相送",  # 多条不会显示
                        "url": "www.qq.com",
                        "picurl": "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
                    },
                    {
                        "title": "中秋节礼品领取2",
                        "description": "今年中秋节公司有豪礼相送",
                        "url": "www.qq.com",
                        "picurl": "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
                    },
                    {
                        "title": "中秋节礼品领取3",
                        "description": "今年中秋节公司有豪礼相送",
                        "url": "www.qq.com",
                        "picurl": "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
                    }
                ]
            }
        }
        self.send(json)

    @staticmethod
    def _convert_hook_url(hook_url):
        if not hook_url.startswith('http'):
            hook_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={hook_url}'
        return hook_url


if __name__ == '__main__':
    bot = Bot()
    # bot.send_news()

    bot.send_news_(Article())