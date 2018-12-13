#!/usr/bin/env python3
# coding=utf-8
import os
import re
import sys
import getopt
import requests
from bs4 import BeautifulSoup
import json
import html2text

# 简书主页
jianshu_root_url = "https://www.jianshu.com/"
# 简书文章页
jianshu_post_url = jianshu_root_url + "p/"
# 简书专题页
jianshu_collection_url = jianshu_root_url + "c/"
# 请求头信息
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "max-age=0",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 "
                  "Safari/537.36",
    "if-none-match": 'W/"3c609bd0d55b942904fe20ef67d7a61f"'
}
# 是否打印抓取详情
verbose = False


def get_collection(url=None, collection_slug=None, page=None):
    # 处理 url
    if url is None:
        if collection_slug is None:
            # TODO 返回值
            sys.exit(2)
        else:
            url = jianshu_collection_url + collection_slug

    # 获取网页源码
    html = requests.get(url=url, headers=headers)
    # TODO 对于非 post 的容错处理
    # 使用 BeautifulSoup 解析网页
    soup = BeautifulSoup(html.text, 'lxml')

    # 提取网页 json 信息
    json_message = soup.findAll('script', attrs={"data-name": "collection", "type": "application/json"})
    json_message = json.loads(json_message[0].text)
    # 记录专题信息
    message = dict()
    # 专题 id
    message['id'] = json_message['id']
    # 专题 slug
    message['slug'] = json_message['slug']
    # 专题作者 id
    message['owner_id'] = json_message['owner']['id']
    # 关注人数
    message['subscribers_count'] = json_message['subscribers_count']
    # 专题简介
    message['content'] = html2text.html2text(json_message['content'])
    # 专题名称
    message['title'] = soup.select('.name')[0].text
    # 收录文章数量
    info = soup.select('.info')[0].text
    message['post_number'] = re.findall("收录了(\d*)篇文章", info)[0]
    # 获取管理员信息
    # 初始化 headers, 当前页码, 总页码
    headers['accept'] = 'application/json'
    administrator_page = 1
    total_page = 1
    administrator_slug_list = []
    # 循环获取管理员信息
    while administrator_page <= total_page:
        # 拼接当前页码 url
        administrator_url = jianshu_root_url + 'collections/' + str(message['id']) + '/editors?page=' + \
                            str(administrator_page)
        # 获取当前页作者 json 数据
        json_data = requests.get(administrator_url, headers=headers).text
        # 解码 json 数据
        json_dict = json.loads(json_data)
        # 获取总页数
        total_page = json_dict['total_pages']

        for i in json_dict['editors']:
            administrator_slug_list.append(i['slug'])

        administrator_page += 1
    del total_page
    # 管理员列表
    message['administrator_slug_list'] = administrator_slug_list

    # TODO 获取作者信息
    # TODO 获取订阅者信息 url = https://www.jianshu.com/collection/25/subscribers?max_sort_id=183941854

    # 计算文章页码
    # 每页文章数量 TODO 可以写进配置文件
    page_per = 10
    post_number = int(message['post_number'])
    total_page = post_number // page_per
    if post_number % page_per != 0:
        total_page += 1
    # 专题文章总页码
    message['total_page'] = total_page

    # 默认只获取第一页文章
    page_from = 1
    page_to = 1
    # 处理 page 参数
    page_arg = dict()
    if page is not None:
        if type(page).__name__ == 'int':
            if page == 0:
                # 下载所有页码
                page_to = total_page
            else:
                # 下载指定页码
                page_from = page
                page_to = page
            page_arg['aim'] = page
        elif type(page).__name__ == 'str':
            if page[: page.index(":")] == "":
                page_from = 1
            else:
                page_from = int(page[: page.index(":")])

            if page[page.index(":") + 1 :] == "":
                page_to = total_page
            else:
                page_to = int(page[page.index(":") + 1 :])

    # 修改请求头信息
    headers['accept'] = 'text/html, */*; q=0.01'
    headers['x-infinitescroll'] = "true"
    headers['x-requested-with'] = "XMLHttpRequest"

    post_slug_list = list()
    for i in range(page_from, page_to + 1):
        note_list_url = 'https://www.jianshu.com/c/' + message['slug'] + '?order_by=added_at&page=' + str(i)
        note_list_html = requests.get(note_list_url, headers=headers)
        note_list_soup = BeautifulSoup(note_list_html.text, 'lxml')
        note_list = note_list_soup.select('a.title')
        for note in note_list:
            # 这里从 href 里面截取了 slug
            post_slug_list.append(note.get('href')[3:])

    # 专题文章 slug 列表
    message['post_slug_list'] = post_slug_list

    # [print(message[key]) for key in message]
    return message


def get_post(url=None, post_slug=None):
    """
    获取单篇文章数据
    :param url: 文章 url
    :param post_slug: 文章 slug
    :return: 文章信息
    """
    # 设置文章 url
    if url is None:
        if post_slug is None:
            # TODO 返回值
            sys.exit(2)
        else:
            url = jianshu_post_url + post_slug
    # 获取网页源码
    html = requests.get(url=url, headers=headers)
    # TODO 对于非 post 的容错处理
    # 使用 BeautifulSoup 解析网页
    soup = BeautifulSoup(html.text, 'lxml')

    # 记录文章信息
    post_message = {}
    # 获取文章标题
    title = soup.select('.article h1')[0].text
    # 获取作者 id
    author_slug = soup.select('.name a')[0].get('href')[3:]
    # 获取最后编辑时间
    publish_time = soup.select(".publish-time")[0].text

    # 解析文章自带 json 信息
    message = soup.findAll('script', attrs={"data-name": "page-data", "type": "application/json"})
    message_json = json.loads(message[0].text)

    # 文章标题
    post_message['title'] = title
    # 作者昵称
    post_message['author_name'] = message_json['note']['author']['nickname']
    # 作者 id
    post_message['author_id'] = message_json['note']['user_id']
    # 作者 slug
    post_message['author_slug'] = author_slug
    # 文章最后编辑时间
    post_message['publish_time'] = publish_time
    # 文章字数统计
    post_message['word_count'] = message_json['note']['public_wordage']
    # 文章阅读数量统计
    post_message['views_count'] = message_json['note']['views_count']
    # 文章所属笔记本 id
    post_message['notebook_id'] = message_json['note']['notebook_id']
    # 文章 id
    post_message['post_id'] = message_json['note']['id']
    # 文章 slug
    post_message['post_slug'] = message_json['note']['slug']
    # 文章喜欢数量统计
    post_message['likes_count'] = message_json['note']['likes_count']
    # 文章是否可评论
    post_message['commentable'] = message_json['note']['commentable']
    # 文章评论数量
    post_message['comments_count'] = message_json['note']['comments_count']
    # 文章内容
    content = soup.select('.show-content')[0]
    # 提取图片并获取真实链接
    images = content.findAll('img')
    for img in images:
        # 先删除可能存在的 src 属性
        img['src'] = "https:" + img['data-original-src']

    # 获取并删除图题
    # TODO 可以尝试把图题转换为 alt 文本
    img_captions = content.select('.image-caption')
    [img_caption.extract() for img_caption in img_captions]

    html2markdown = html2text.HTML2Text()
    markdown = html2markdown.handle(str(content))
    # 修复 html2text 错误换行
    # TODO 这里需要优化, 只针对 a 标签和图片标签换行即可
    markdown = markdown.replace('-\n', '-')
    # 添加文章内容
    post_message['content'] = markdown

    return post_message


def cli_arguments(argv):
    """
    处理命令行参数
    :param argv: 命令行参数
    :return: None
    """
    # 解析参数列表
    try:
        opts, args = getopt.getopt(argv, "hv", ["post-url=",
                                                "post-slug=",
                                                "output=",
                                                "collection-url=",
                                                "collection-slug=",
                                                "page="
                                                ])
    except getopt.GetoptError as e:
        print(e.msg)
        sys.exit(2)

    # TODO 解析 args 参数, 比如自动判断 url 类型
    # for arg in args:

    # 初始化变量
    process = None
    post_url = None
    post_slug = None
    collection_url = None
    collection_slug = None
    page = None
    output = "./"

    # TODO 处理文件输出
    for opt, arg in opts:
        if opt == '-v':
            global verbose
            verbose = True
        elif opt == '-h':
            show_help()
            sys.exit()
        elif opt == '--post-url':
            process = "post"
            post_url = arg
        elif opt == '--post-slug':
            process = "post"
            post_slug = arg
        elif opt == '--collection-url':
            process = "collection"
            collection_url = arg
        elif opt == '--collection-slug':
            process = "collection"
            collection_slug = arg
        elif opt == '--page':
            # 设置页码
            page = arg
        elif opt == '--output':
            output = arg
        else:
            print('Wrong arguments')
            sys.exit()

    # 执行程序
    if process == "post":
        post = get_post(post_url, post_slug)
        write_post(post, output)
        print("执行完毕")
    elif process == "collection":
        collection = get_collection(collection_url, collection_slug, page)
        output += collection.get('title')
        for i in collection.get('post_slug_list'):
            write_post(get_post(post_slug=i), output)
        print("执行完毕")
    else:
        print("未知流程")
        sys.exit()


def show_help():
    """
    显示帮助信息
    :return: None
    """
    # TODO 多个参数值用 , 分割,比如多个 slug 或者 url
    help_message = '''
    抓取简书文章/专题/文集/作者信息
    参数介绍: 
        -h      显示帮助信息
        -v      详细模式, 输出抓取信息
        --post-url      文章链接
                            此参数与 post-slug 二选一即可
        --post-slug     文章标识
                            此参数与 post-url 二选一即可
        --collection-url    专题链接
                                此参数与 collection-slug 二选一即可
        --collection-slug   专题标识
                                此参数与 collection-url 二选一即可
        --page          指定抓取页码
                            0 表示抓取全部
                            n 表示抓取第 n 页
                            n:m 表示抓取第 n 页到第 m 页
        --output        指定输出目录
                            默认为当前目录
    '''
    print(help_message)


def write_post(post, output='./'):
    """
    将单篇文章写入文件
    :param post: 文章数据
    :param output: 输出目录
    :return: None
    """
    post_content = post.pop('content')
    # TODO output 容错
    # 检查文件夹是否存在
    if not os.path.exists(output):
        os.mkdir(output)
    # 定义文件名
    file_path = output + "/" + post['title'] + ".md"
    with open(file_path, "w") as f:
        f.write("---\n")
        # 写入文章元数据
        [f.write(i + ":\t" + str(post.get(i)) + "\n") for i in post]
        f.write("\n---\n")
        # 写入文章内容
        f.write(post_content)


if __name__ == "__main__":
    cli_arguments(sys.argv[1:])
