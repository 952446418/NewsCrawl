import os
import re

import requests
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from movie1.items import Movie1Item
from redis import Redis

import movie1.GlobalVar
from multiprocessing.dummy import Pool

from 爬虫代码.pachong.军事视频代码.jinritoutiao.今日头条5_scrapy框架搭建.movie1.movie1.items import Movie1Item


def download(web, urls):
    pool = Pool(4)
    print(urls)
    # if web == '哔哩哔哩':
    #     pool.map(bilibili_get_video_data, urls)
    # elif web == '今日头条':
    pool.map(jinritoutiao_get_video_data, urls)
    pool.close()
    pool.join()


# 视频下载方面的函数
def jinritoutiao_get_video_data(dic):
    directory = '视频'
    filename = dic['title']
    url = dic['video_url']
    filename = sanitize_filename(filename)
    print(filename, '正在下载......')
    headers = {'User-Agent': movie1.GlobalVar.user_agent}
    data = requests.get(url=url, headers=headers).content
    # with open('./视频/' + filename + '.mp4', 'wb') as fp:
    # 如果目录不存在，则创建
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open('./视频/' + filename + '.mp4', 'wb') as fp:
        fp.write(data)
        print(filename, '下载成功')


def sanitize_filename(filename):
    # 定义不合规字符的正则表达式
    invalid_chars_regex = r'[\"*<>?\\|/:,]'
    # 替换不合规字符为空格
    sanitized_filename = re.sub(invalid_chars_regex, ' ', filename)
    return sanitized_filename

class Movie1Spider(CrawlSpider):
    name = "movie"

    # def __init__(self, key=None):
    #     super(Movie1Spider, self).__init__()
    #     self.key = key
    #     print(self.key)
    #     start_url = 'https://so.toutiao.com/search?dvpf=pc&source=pagination&keyword=%s&pd=video&page_num=0&action_type=search_subtab_switch&search_id=&from=video&cur_tab_title=video' % self.key
    #     self.start_urls = [start_url]
    #     # 链接提取器：根据指定规则（allow="正则"）进行指定链接的提取
    #     # link = LinkExtractor(allow=r'((?!wid_ct).).*dvpf=pc&source=pagination&keyword=.*pd=video&page_num=\d+')
    #     link = LinkExtractor(allow=r'wid_ct=.*dvpf=pc&source=pagination&keyword=.*pd=video&page_num=\d+')
    #     rules = (
    #         # 规则解析器:将链接提取器提取到的链接进行指定规则（callback）的解析操作
    #         Rule(link, callback="parse_item", follow=True),
    #     )
    #     self.rules = rules

    keyword = '乌克兰'
    # allowed_domains = ["www.xxx.com"]
    # start_url = "https://so.toutiao.com/search?dvpf=pc&source=search_subtab_switch&keyword=" + keyword + "&pd=video&page_num=0&action_type=search_subtab_switch&search_id=&from=video&cur_tab_title=video"
    start_url = "https://so.toutiao.com/search?dvpf=pc&source=pagination&keyword=" + keyword + "&pd=video&page_num=0&action_type=search_subtab_switch&search_id=&from=video&cur_tab_title=video"

    start_urls = [start_url]

    # 链接提取器：根据指定规则（allow="正则"）进行指定链接的提取
    # link = LinkExtractor(allow=r'((?!wid_ct).).*dvpf=pc&source=pagination&keyword=.*pd=video&page_num=\d+')
    link = LinkExtractor(allow=r'wid_ct=.*dvpf=pc&source=pagination&keyword=.*pd=video&page_num=\d+')
    rules = (
        # 规则解析器:将链接提取器提取到的链接进行指定规则（callback）的解析操作
        Rule(link, callback="parse_item", follow=True),
    )

    # # allowed_domains = ["www.xxx.com"]
    # start_urls = ["https://www.xxx.com"]
    # keyword = '乌克兰'
    # allowed_domains = ["www.xxx.com"]
    # start_url = "https://so.toutiao.com/search?dvpf=pc&source=search_subtab_switch&keyword=" + keyword + "&pd=video&page_num=0&action_type=search_subtab_switch&search_id=&from=video&cur_tab_title=video"

    video_urls = []  # 存储所有视频对应的url
    urls = []  # 存储所有视频的链接和文件名

    conn = Redis(host='127.0.0.1', port=6379)

    # 更新：这个不需要重新加__init__
    s = Service('E:\个人\代码\爬虫代码\pachong\军事视频代码\jinritoutiao\chromedriver.exe')
    driver = webdriver.Chrome(service=s)
    a = 0

    def parse_item(self, response):
        # 打印当前处理的URL
        print(f"Processing URL: {response.url}")

        # # 检查是否成功下载了页面
        # if response.status != 200:
        #     print(f"Failed to download page: {response.url} - Status Code: {response.status}")

        # item = {}
        # self.a += 1
        # print(self.a)
        # print(response)
        # # return item

        # print('url:')
        # print(response.request.url)
        div_list = None
        div_list = response.xpath(
            # '/html/body/div[2]/div[2]/div[1]/div')  # 这里的xpath不很智能，只能用一点点xpath然后再分别取href（也可能不适合class搜索）
            '/html/body/div[2]/div[2]/div[1]/div[2]')  # 这里的xpath不很智能，只能用一点点xpath然后再分别取href（也可能不适合class搜索）
        # '//*[@class="cs-view cs-view-block cs-grid-cell grid-cell-3 grid-cell-x-m grid-cell-y-m"]/div/div/div[1]/div/div/a/@href').extract()
        # print(div_list)
        for url in div_list:
            # 获取详情页url
            url_list = url.xpath('./div/div/div[1]/div/div/a/@href').extract_first()
            div_url_id = re.search(r"www.toutiao.com%2Fa(.*?)%2F%3Fchannel", url_list)
            # print(div_url_id.group(1))
            video_url = 'https://www.toutiao.com/video/' + str(div_url_id.group(1)) + '/?channel=&source=video'
            # print(video_url)
            # video_url = 'https://so.toutiao.com' + url_list

            # 将的url存入redis的set中
            ex = self.conn.sadd('urls', video_url)  # urls为redis库名——爬取过的url
            # print('ex:')
            # print(ex)
            # if ex == 1:
            #     print('该url没有被爬取过，可以进行数据爬取')
            #
            #     # print(video_url_list)
            #     #     self.video_urls.append(video_url)
            #     #
            #     # # print(self.video_urls)
            #     #
            #     # # 一次对每个视频详情页发起请求
            #     # for url_list in self.video_urls:
            #     # video_url = 'https://so.toutiao.com' + url_list
            #     yield scrapy.Request(video_url, callback=self.parse_video)
            #
            # else:
            #     print('数据还没有更新，暂无新数据可爬取')
            yield scrapy.Request(video_url, callback=self.parse_video)

    def parse_video(self, response):  # 解析每个页面中视频链接
        self.a += 1
        print(self.a)

        title = response.xpath('/html/head/title/text()').extract_first()
        # print(title)
        video_url = response.xpath(
            '///*[@id="root"]/div/div[2]/div[1]/div/div[1]/ul/li[2]/div/video/@src').extract_first()
        src_url = 'https:' + str(video_url)
        # print(src_url)

        item = Movie1Item()
        item['id'] = self.a
        item['title'] = title
        item['video_url'] = src_url

        dic = {
            'title': title,
            'video_url': src_url
        }

        print(f"dic : {dic}")
        self.urls.append(dic)
        print(f"urls : {self.urls}")

        # 9.18可加功能——当url有blob要从script里找json串，转换后得到真实url（如果不行可以sele在线json解析网页得到返回数据
        yield item



    def closed(self, spider):
        download(web='今日头条', urls=self.urls)
        self.driver.quit()





