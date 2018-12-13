### 简介
    python 脚本, 用于抓取简书文章/专题/文集/作者信息
    
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

### 依赖

    依赖 requests, re, sys, getopt, requests, bs4, json, html2text


### 举例

* 显示帮助信息

    ```shell
    python jianshu.py -h
    ```

* 抓取单篇文章

    * 使用 url 抓取:

        ```shell
        python jianshu.py --post-url https://www.jianshu.com/p/5bd14cbf7186
        ```

    * 使用 slug 抓取:

        ```shell
        python jianshu.py --post-slug 5bd14cbf7186
        ```

    * 指定文章保存目录

        ```shell
        python jianshu.py --post-slug 5bd14cbf7186 --output /home/seven/Downloads/
        ```

* 抓取专题

    * 通过 url 抓取专题

        ```shell
        python jianshu.py --collection-url https://www.jianshu.com/c/e048f1a72e3d
        ```

    * 通过 slug 抓取专题

        ```shell
        python jianshu.py --collection-slug e048f1a72e3d
        ```

    * 抓取专题所有文章

        ```shell
        python jianshu.py --collection-slug e048f1a72e3d --page 0
        ```

        ```shell
        python jianshu.py --collection-slug e048f1a72e3d --page :
        ```

        ```shell
        python jianshu.py --collection-slug e048f1a72e3d --page 1:
        ```

    * 抓取专题特定页码文章

        ```shell
        # 抓取指定专题第 2 页文章
        python jianshu.py --collection-slug e048f1a72e3d --page 2
        ```

    * 抓取专题范围页码文章

        ```shell
        # 抓取指定专题第 2 页到第 5 页文章
        python jianshu.py --collection-slug e048f1a72e3d --page 2:5
        ```

    * 指定文章保存目录

        ```shell
        python jianshu.py --collection-slug e048f1a72e3d --page 1 --output /home/seven/Downloads
        ```

