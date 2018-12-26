### 进度

方便统一概念, 这个是自己对简书架构的理解分析:  [简书架构解析](https://mubu.com/doc/btsI4SKpAH) 

目前已完成单一文章内容抓取, 指定专题文章抓取, 指定用户文章抓取

#### TODO List

* 将各种配置项提取到配置文件

* 尝试将分页内容也封装成函数, 如文章, 用户列表等

* 7 日热门抓取

* 30 日热门抓取

* 简书标签页抓取

* 多线程抓取

* 代理 ip 池

### 简介

    python 脚本, 用于抓取简书文章/专题/文集/作者信息

    参数介绍:
        -h                  显示帮助信息
        -v                  详细模式, 输出抓取信息
        --post-url          文章链接
                                此参数与 post-slug 二选一即可
        --post-slug         文章标识
                                此参数与 post-url 二选一即可
        --user-url          用户主页连接
                                此参数与 user-slug 二选一即可
        --user-slug         用户标识
                                此参数与 user-url 二选一即可
        --collection-url    专题链接
                                此参数与 collection-slug 二选一即可
        --collection-slug   专题标识
                                此参数与 collection-url 二选一即可
        --page              指定抓取页码
                                不指定 page 参数时, 默认只抓取第一页内容
                                0 表示抓取全部
                                n 表示抓取第 n 页
                                n:m 表示抓取第 n 页到第 m 页
        --output            指定输出目录
                                不指定 output 参数时, 默认为当前目录

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
    
* 抓取用户文章

    * 通过 url 抓取:
    
        ```shell
        python jianshu.py --user-url https://www.jianshu.com/u/474f4a8db16f
        ```
    
    * 通过 slug 抓取:
    
        ```shell
        python jianshu.py --user-slug 474f4a8db16f
        ```
    
    * 指定文章保存目录
      
        ```shell
        python jianshu.py --user-slug 474f4a8db16f --output /usr/seven/Downloads/
        ```
    
    * 指定页码
    
        ```shell
        # 抓取用户第 1 页 到第 3 页文章内容
        python jianshu.py --user-slug 474f4a8db16f --page 1:3
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

* 抓取文集 / 连载

    * 通过 url 抓取文集 / 连载
    
        ```shell
        python jianshu.py --notebook-url https://www.jianshu.com/nb/12010430
        ```
    
    * 通过 slug 抓取文集 / 连载
    
        ```shell
        python jianshu.py --notebook-slug 12010430
        ```
    
    * 抓取特定页码的文集 / 连载
    
        ```shell
        python jianshu.py --notebook-slug 12010430 --output /home/seven/Downloads
        ```

    * 抓取范围页码的文集 / 连载
    
        * 抓取文集 / 连载全部文章
        
            ```shell
            python jianshu.py --notebook-slug 12010430 --page 0 --output /home/seven/Downloads
            ```

        * 抓取文集 / 连载第 2 - 5 页全部文章
        
            ```shell
            python jianshu.py --notebook-slug 12010430 --page 2:5 --output /home/seven/Downloads
            ```
        
    * 指定文章保存路径
    
        * 抓取文集 / 连载特定页码文章

            ```shell
            # 抓取文集第二页所有文章
            python jianshu.py --notebook-slug 12010430 --page 2 --output /home/seven/Downloads
            ```

* 抓取 "7 日热门"
    
    * 默认只抓取第一页 20 篇文章
        
        ```shell
        python jianshu.py --weekly
        ```
        
    * 抓取特定页码文章
    
        ```shell
        # 指定抓取第二页文章
        python jianshu.py --weekly --page 2
        ```
        
    * 抓取范围页码文章
    
        ```shell
        python jianshu.py --weekly --page 3:6
        ```

    * 指定文章保存路径
    
        ```shell
        python jianshu.py --weekly --output ~/Downloads
        ```    
    
* 抓取 "30 日热门"
        
    * 默认只抓取第一页 20 篇文章
        
        ```shell
        python jianshu.py --monthly
        ```
        
    * 抓取特定页码文章
    
        ```shell
        # 指定抓取第二页文章
        python jianshu.py --monthly --page 2
        ```
        
    * 抓取范围页码文章
    
        ```shell
        python jianshu.py --monthly --page 3:6
        ```
        
    * 指定文章保存路径
    
        ```shell
        python jianshu.py --monthly --output ~/Downloads
        ```    
