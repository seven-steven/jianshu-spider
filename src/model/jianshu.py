# coding=utf-8

import requests
from bs4 import BeautifulSoup
import json

# 简书主页
jianshu_root = "https://www.jianshu.com/"
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "max-age=0",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 "
                  "Safari/537.36",
    "if-none-match": 'W/"3c609bd0d55b942904fe20ef67d7a61f"'
}


def get_post(url=None, post_id=None):
    # 设置文章 url
    if url is None:
        if post_id is None:
            # TODO 返回值
            return 1
        else:
            url = jianshu_root + r"p/" + post_id
    # 获取网页源码
    # html = requests.get(url=url, headers=headers)
    # 使用 BeautifulSoup 解析网页
    # soup = BeautifulSoup(html.text, 'lxml')
    soup = BeautifulSoup(open('post.html'), 'lxml')

    post_message = {}
    # 获取文章标题
    title = soup.title.string
    # 获取作者信息
    author = soup.select('.name a')
    # 获取作者名称
    author_name = author[0].text
    # 获取作者 id
    author_id = author[0].get('href')[3:]
    # 获取最后编辑时间
    publish_time = soup.select(".publish-time")[0].text
    # 获取文章字数统计
    word_count = soup.select(".wordage")[0].text[3:]

    message = soup.findAll('script', attrs={"data-name": "page-data", "type": "application/json"})
    message_json = json.loads(message[0].text)
    # print(message_json)
    print(message[0].text)
    # print(message_json['locale'])


    post_message['title'] = title
    post_message['author_name'] = author_name
    post_message['author_id'] = author_id
    post_message['publish_time'] = publish_time
    post_message['word_count'] = word_count
    # print(post_message)


if __name__ == "__main__":
    get_post(post_id='6f1e68d1b7a1')
