SCRAPY\_BOX
===========

简单好用的scrapy插件盒

download middlewares
--------------------

-  代理下载中间件

   .. code:: python

       # 代理url
       PROXY_ADDR = 'your proxy API'

-  错误重定向重试的下载中间件

   .. code:: python

       # 需要对重定向的url,使用原url进行重试的url片段
       ERROR_REDIRECT_URL_SNIPPET = ['redirect', 'retry']
       # 注意，数字必须大于600
       DOWNLOADER_MIDDLEWARES = {
          'scrapy_box.ErrorRedirectMiddleware': 601,
       }
