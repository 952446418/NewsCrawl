import scrapy
from redis.client import Redis
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from movie.items import MovieItem

class MovieSpider(CrawlSpider):
    name = "movie2"
    # # allowed_domains = ["www.xxx.com"]
    # start_urls = ["https://www.xxx.com"]
    keyword = '乌克兰'
    # allowed_domains = ["www.xxx.com"]
    # start_url = "https://so.toutiao.com/search?dvpf=pc&source=search_subtab_switch&keyword=" + keyword + "&pd=video&page_num=0&action_type=search_subtab_switch&search_id=&from=video&cur_tab_title=video"
    start_url = "https://so.toutiao.com/search?dvpf=pc&source=pagination&keyword=" + keyword + "&pd=video&page_num=0&action_type=search_subtab_switch&search_id=&from=video&cur_tab_title=video"

    start_urls = [start_url]

    video_urls = []  # 存储所有视频对应的url

    # 链接提取器：根据指定规则（allow="正则"）进行指定链接的提取
    # link = LinkExtractor(allow=r'((?!wid_ct).).*dvpf=pc&source=pagination&keyword=.*pd=video&page_num=\d+')
    link = LinkExtractor(allow=r'wid_ct=.*dvpf=pc&source=pagination&keyword=.*pd=video&page_num=\d+')
    rules = (
        # 规则解析器:将链接提取器提取到的链接进行指定规则（callback）的解析操作
        Rule(link, callback="parse_item", follow=True),
    )
    conn = Redis(host='127.0.0.1', port=6379)
    # 将的url存入redis的set中
    ex = conn.sadd('urls', '1')  # urls为redis库名——爬取过的url

    def __init__(self):
        super(MovieSpider, self).__init__()
        s = Service('E:\个人\代码\爬虫代码\pachong\军事视频代码\jinritoutiao\chromedriver.exe')
        self.driver = webdriver.Chrome(service=s)
        self.a = 0

    def parse_item(self, response):
        # item = {}
        # self.a += 1
        # print(self.a)
        # print(response)
        # # return item

        div_list = response.xpath(
            # '/html/body/div[2]/div[2]/div[1]/div[1]')  # 这里的xpath不很智能，只能用一点点xpath然后再分别取href（也可能不适合class搜索）
            '/html/body/div[2]/div[2]/div[1]/div')  # 这里的xpath不很智能，只能用一点点xpath然后再分别取href（也可能不适合class搜索）

        # '//*[@class="cs-view cs-view-block cs-grid-cell grid-cell-3 grid-cell-x-m grid-cell-y-m"]/div/div/div[1]/div/div/a/@href').extract()
        # print(div_list)
        for url in div_list:
            url_list = url.xpath('./div/div/div[1]/div/div/a/@href').extract_first()
            video_url_list = 'https://so.toutiao.com' + url_list
            # print(video_url_list)
            self.video_urls.append(video_url_list)

        # print(self.video_urls)

        # 一次对每个视频详情页发起请求
        for url in self.video_urls:
            # video_url = 'https://so.toutiao.com' + url
            yield scrapy.Request(url, callback=self.parse_video)

    def parse_video(self, response):  # 解析每个页面中视频链接
        self.a += 1
        print(self.a)

        title = response.xpath('/html/head/title/text()').extract_first()
        # print(title)
        video_url = response.xpath(
            '///*[@id="root"]/div/div[2]/div[1]/div/div[1]/ul/li[2]/div/video/@src').extract_first()
        src_url = 'https:' + str(video_url)
        # print(src_url)

        item = MovieItem()
        item['id'] = self.a
        item['title'] = title
        item['video_url'] = src_url

        # 9.18可加功能——当url有blob要从script里找json串，转换后得到真实url（如果不行可以sele在线json解析网页得到返回数据
        yield item

    # def closed(self, spider):
    #     self.driver.quit()

    # 解析五大板块对应的详情页url
    # def parse(self, response):
    #     div_list = response.xpath(
    #         '/html/body/div[2]/div[2]/div[1]/div')  # 这里的xpath不很智能，只能用一点点xpath然后再分别取href（也可能不适合class搜索）
    #     # '//*[@class="cs-view cs-view-block cs-grid-cell grid-cell-3 grid-cell-x-m grid-cell-y-m"]/div/div/div[1]/div/div/a/@href').extract()
    #     # print(div_list)
    #     for url in div_list:
    #         url_list = url.xpath('./div/div/div[1]/div/div/a/@href').extract_first()
    #         video_url_list = 'https://so.toutiao.com' + url_list
    #         # print(video_url_list)
    #         self.video_urls.append(video_url_list)
    #
    #     # print(self.video_urls)
    #
    #     # 一次对每个视频详情页发起请求
    #     for url in self.video_urls:
    #         # video_url = 'https://so.toutiao.com' + url
    #         yield scrapy.Request(url, callback=self.parse_video)
