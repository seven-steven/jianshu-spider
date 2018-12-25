# 简书主页
jianshu_root_url = "https://www.jianshu.com/"
# 简书文章页
jianshu_post_url = jianshu_root_url + "p/"
# 简书专题页
jianshu_collection_url = jianshu_root_url + "c/"
# 简书用户主页
jianshu_user_url = jianshu_root_url + "u/"
# 简书文集/连载页面
jianshu_notebook_url = jianshu_root_url + "nb/"
# 请求头信息
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    # "cache-control": "max-age=0",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 "
                  "Safari/537.36",
    # "if-none-match": 'W/"3c609bd0d55b942904fe20ef67d7a61f"'
}

# 每页文章数量
post_per_page = 10