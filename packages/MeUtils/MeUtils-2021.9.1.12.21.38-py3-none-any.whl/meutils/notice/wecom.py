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


class Article(BaseConfig):
    title: str = '百度热榜'
    description: str = '百度热榜'
    url: str = 'https://top.baidu.com/board?tab=realtime'
    picurl: str = 'http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png'


class Wecom(object):

    def __init__(self, hook_url='1eb25317-39a1-4af7-a6e3-63877ec2dd64'):
        self.hook_url = self._convert_hook_url(hook_url)

    def send_markdown(self, title="", content=""):

        if isinstance(content, (list, tuple)):
            content = '\n'.join(content).strip()

        json = {
            "msgtype": "markdown",
            "markdown": {
                "content": f"{title}\n\n{content}".strip()
            }
        }
        return self._send(json)

    def send_text(self, title="", content="", mentioned_mobile_list=None):
        json = {
            "msgtype": "text",
            "text": {
                "content": f"{title}\n{content}".strip()
            }
        }
        if mentioned_mobile_list:  # "@all"'
            json['text']['mentioned_mobile_list'] = mentioned_mobile_list

        return self._send(json)

    def send_news(self, articles: Union[Article, List[Article]]):
        """
        json = {
        "msgtype": "news",
        "news": {
        "articles": [
            {
                "title": "中秋节礼品领取1",
                "description": "今年中秋节公司有豪礼相送",  # 多条不会显示
                "url": "www.qq.com",
                "picurl": "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
            }
        ]}}
        """
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
        return self._send(json)

    def send_image(self, path='http://www.nesc.cn/dbzq/images/logo.png'):
        bytes_data = self._get_bytes(path)
        body = {
            "msgtype": "image",
            "image": {
                "base64": bytes2base64(bytes_data),
                "md5": md5(bytes_data, False)
            }
        }
        return self._send(body)

    def send_file(self, path, type='file'):
        upload_media_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={self.key}&type={type}'

        # bytes_data = self.get_bytes(path)
        # files = {'data': bytes_data} # 这样文件名为data

        with open(path, 'rb') as f:
            files = {'data': f}
            response = requests.post(upload_media_url, files=files)

        media_id = response.json()['media_id']

        body = {"msgtype": type, type: {"media_id": media_id}}
        return self._send(body)

    def _send(self, body=None):
        if body is None:
            body = {
                "msgtype": "text",
                "text": {
                    "content": "南京今日天气：29度，大部分多云，降雨概率：60%",
                    "mentioned_mobile_list": ["18550288233", "@all"]
                }
            }
        return requests.post(url=self.hook_url, json=body)

    @staticmethod
    def _get_bytes(path):
        if path.startswith('http'):
            bytes_data = requests.get(path).content
        else:
            bytes_data = Path(path).read_bytes()
        return bytes_data

    @staticmethod
    def _convert_hook_url(hook_url):
        if not hook_url.startswith('http'):
            hook_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={hook_url}'
        return hook_url


if __name__ == '__main__':
    wecom = Wecom()
    wecom.send_news(Article())
