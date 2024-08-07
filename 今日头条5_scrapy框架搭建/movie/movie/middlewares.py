# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from scrapy.http import HtmlResponse
import time
import re
from random import *


class MovieDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    # 更新：这个不需要重新加__init__
    # def __init__(self):
    #     super(MovieDownloaderMiddleware, self).__init__()
    #     self.a = 0
    #     self.changed_url_list = []
    a = 0
    changed_url_list = []
    conn = None

    def open_spider(self, spider):
        self.conn = spider.conn

    def process_request(self, request, spider):

        # search_url_keywords = 'search_id='
        # search_url_ex_start_keywords = '&search_id=&from=video'

        # old_url = request.url
        # new_url = request.url.replace("str", "") + "str"
        # request._set_url(new_url)

        # if search_url_keywords in request.url and not search_url_ex_start_keywords in request.url and not request.url in self.changed_url_list:
        #     print('网址包含search_id=字段')
        #     url = request.url
        #     self.changed_url_list.append(url)
        #
        #     str0 = url.split('search_id=')[-1]
        #     str1 = url.split('search_id=')[0]
        #     print(str0)
        #     new_url = str1 + 'search_id=' + f'{str0[:13]}{randint(0, 9)}{str0[14:]}'
        #     # self.a += 1
        #     print('原网址为:' + request.url)
        #     print('新网址为:' + new_url)
        #
        #     request._set_url(new_url)

        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    # 该方法拦截五大板块对应的响应对象，进行篡改
    def process_response(self, request, response, spider):  # spider爬虫对象
        driver = spider.driver  # 获取了爬虫类中定义的浏览器对象
        # 挑选出指定的相应对象进行篡改
        # 通过url指定request
        # 通过request指定response
        print('request的url：')
        print(request.url)
        # start_url_keywords = 'https://so.toutiao.com/search?dvpf=pc&source=search_subtab_switch&keyword='
        start_url_keywords = "dvpf=pc&source=pagination&keyword="
        video_url_keywords1 = 'https://www.toutiao.com/video/'
        video_url_keywords2 = '/?channel=&source=video'
        search_url_keywords = 'search_id='
        search_url_ex_start_keywords = '&search_id=&from=video'  # 这是初始url的部分，需要排除掉该url不需要改日期

        # if search_url_keywords in request.url and search_url_ex_start_keywords not in request.url:
        #     print('网址包含search_id=字段')
        #     url = request.url
        #     # 将的url存入redis的set中
        #     ex = self.conn.sadd('list_urls', url)  # urls为redis库名——爬取过的url
        #     # self.changed_url_list.append(url)
        #
        #     str0 = url.split('search_id=')[-1]
        #     str1 = url.split('search_id=')[0]
        #     print(str0)
        #     new_url = str1 + 'search_id=' + f'{str0[:13]}{randint(0, 9)}{str0[14:]}'  # 这里仅仅是将秒最后一位随机变换，也可以获取现在的时间进行替换
        #     # self.a += 1
        #     print('原网址为:' + request.url)
        #     print('新网址为:' + new_url)
        #
        #     driver.get(new_url)  # 初始url
        #     # driver.implicitly_wait(2)
        #     time.sleep(3)
        #     page_text = driver.page_source  # 包含了动态加载的搜索页面
        #     # print(page_text)
        #     # response——搜索页面的响应对象
        #     # 针对定位到的response进行篡改
        #     # 实例化一个新的响应对象（包含动态加载的页面），代替原来旧的响应对象
        #     # 如何获取动态加载的数据————基于selenium便捷的获取动态加载数据
        #     new_response = HtmlResponse(url=new_url, body=page_text, encoding='utf-8', request=request)
        #     return new_response

        # elif request.url in spider.video_urls:
        #     driver.get(request.url)  # 初始url
        #     # driver.implicitly_wait(2)
        #     time.sleep(3)
        #     page_text = driver.page_source  # 包含了动态加载的搜索页面
        #     # print(page_text)
        #     # response——搜索页面的响应对象
        #     # 针对定位到的response进行篡改
        #     # 实例化一个新的响应对象（包含动态加载的页面），代替原来旧的响应对象
        #     # 如何获取动态加载的数据————基于selenium便捷的获取动态加载数据
        #     new_response = HtmlResponse(url=request.url, body=page_text, encoding='utf-8', request=request)

        if search_url_ex_start_keywords in request.url or (
                video_url_keywords1 in request.url and video_url_keywords2 in request.url):
            # url = request.url
            # if('wid_ct=' in request.url):
            #     url = re.sub('wid_ct=.{13}','',request.url)
            driver.get(request.url)  # 初始url
            # driver.implicitly_wait(2)
            time.sleep(3)
            page_text = driver.page_source  # 包含了动态加载的搜索页面
            # print(page_text)
            # response——搜索页面的响应对象
            # 针对定位到的response进行篡改
            # 实例化一个新的响应对象（包含动态加载的页面），代替原来旧的响应对象
            # 如何获取动态加载的数据————基于selenium便捷的获取动态加载数据
            new_response = HtmlResponse(url=request.url, body=page_text, encoding='utf-8', request=request)
            return new_response
        # elif search_url_ketwords in request.url:
            # print('网址包含search_id=字段')
            # url = request.url
            #
            # str0 = url.split('search_id=')[-1]
            # print(str0)
            # new_url = f'{str0[:13]}{randint(0,9)}{str0[14:]}'
            # # self.a += 1
            # print('原网址为:' + request.url)
            # print('新网址为:' + new_url)

        else:
            return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass
