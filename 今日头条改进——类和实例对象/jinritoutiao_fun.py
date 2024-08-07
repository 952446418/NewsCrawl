# 此为今日头条4_函数化最终版！！！！！
# 未完成任务——今日头条不能直接得到url的通过import urllib.parse后的print(urllib.parse.unquote(str))函数可以得到，进而在video_list的backup_url找到链接

# 今日头条和哔哩哔哩视频爬取下载并封装为函数
# 线程池并行视频保存（时间19.6s）

from multiprocessing.dummy import Pool
from time import sleep
import random
import requests
import urllib.request
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# import bilibili
import re
import os
import json
from bs4 import BeautifulSoup


class GetUrls:

    def __init__(self):

        self.__web_url = ''
        self.__search_btn_url = ''
        self.__video_list_url = ''

        self.web_name = None
        self.__one_user_agent = self.__get_one_user_agent()
        # print(one_user_agent)
        self.__headers = {'User-Agent': self.__one_user_agent}

        option = webdriver.ChromeOptions()
        # #设置无头模式
        # option.add_argument("--headless")

        # 关闭左上方 Chrome 正受到自动测试软件的控制的提示
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)

        # 设置user-agent
        # option.add_argument('user-agent=' + headers['User-Agent'])
        option.add_argument('user-agent=' + self.__one_user_agent)

        # self.__driver = webdriver.Chrome(options=option)
        s = Service('./chromedriver.exe')
        self.__driver = webdriver.Chrome(service=s, options=option)
        # self.__driver = webdriver.Chrome(service=s)

    @staticmethod
    def __get_one_user_agent():
        with open('./user_agent_all_ok.txt', 'r', encoding='utf-8') as file:
            ret = file.readlines()
        user_agent_list = [i.strip() for i in ret]
        one_user_agent = random.choice(user_agent_list)
        return one_user_agent

    @staticmethod
    def __error():
        print('您输入的参数有误，请填写正确的参数')

    def __get_bilibili_video_audio(self, bid):
        # 构造视频链接并发送请求获取页面内容
        url = f'https://www.bilibili.com/video/{bid}?spm_id_from=333.851.b_7265636f6d6d656e64.6'
        content = requests.get(url, headers=self.__headers).content.decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')

        # 获取视频标题
        meta_tag = soup.head.find('meta', attrs={'name': 'title'})
        title = meta_tag['content']

        # 获取视频和音频链接
        pattern = r'window\.__playinfo__=({.*?})\s*</script>'
        json_data = re.findall(pattern, content)[0]
        data = json.loads(json_data)

        video_url = data['data']['dash']['video'][0]['base_url']
        audio_url = data['data']['dash']['audio'][0]['base_url']
        print(video_url)
        return {
            'title': title,
            'video_url': video_url,
            'audio_url': audio_url
        }

    def main_request(self, web_name, web_url=None):
        if web_url is None:
            if web_name == '今日头条':
                web_url = 'https://www.toutiao.com/'
            elif web_name == '哔哩哔哩':
                web_url = 'https://www.bilibili.com/'
            else:
                self.__error()

        self.__driver.get(web_url)
        self.__driver.implicitly_wait(2)

    def input_key(self, web_name, key, search_btn_xpath=None):
        # 主页搜索框搜索.....
        # search_input = self.__driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div/div[1]/input')
        search_input = self.__driver.find_element(By.XPATH, '//div[@class="search"]/input')
        search_input.send_keys(key)

        if search_btn_xpath is None:
            if web_name == '今日头条':
                search_btn_xpath = '//*[@id="root"]/div/div[4]/div/div[1]/button'
            elif web_name == '哔哩哔哩':
                search_btn_xpath = '//*[@id="nav-searchform"]/div[2]'
            else:
                self.__error()

        # 主页搜索按钮点击
        btn = self.__driver.find_element(By.XPATH, value=search_btn_xpath)
        btn.click()
        # sleep(2)
        self.__driver.implicitly_wait(2)

    def current_window(self):
        # 更新self.__driver页面数据到新的页面（主界面——搜索界面）
        handle = self.__driver.window_handles
        self.__driver.switch_to.window(handle[-1])

        # 更新url到现在页面——搜索界面

        self.__driver.implicitly_wait(2)

        handle_main1 = self.__driver.current_window_handle  # 句柄

        return handle_main1

    def video_btn_click(self, web_name):
        # 今日头条点击到“视频”界面
        if web_name == '今日头条':
            video_btn = self.__driver.find_element(By.XPATH,
                                                   value='//*[@class="cs-view cs-view-flex align-items-center '
                                                         'flex-row"]/a[3]')
            video_btn.click()
            self.__driver.implicitly_wait(2)

    def video_list(self, web_name, video_list_xpath=None):
        if video_list_xpath is None:
            if web_name == '今日头条':
                video_list_xpath = '//*[@class="cs-view cs-view-block cs-grid-cell grid-cell-3 grid-cell-x-m ' \
                                   'grid-cell-y-m"]/div/div/div[1]'
            elif web_name == '哔哩哔哩':
                video_list_xpath = '//*[@class="video-item matrix"]/a'
            else:
                self.__error()
        video_list = self.__driver.find_elements(By.XPATH, value=video_list_xpath)
        return video_list

    def video_url_list(self, web_name, video_list, handle_main):
        index = 0
        urls = []  # 存储所有视频的链接和文件名
        bids = []
        for video in video_list:
            video.click()
            a = random.random() * 3
            sleep(a)  # 设置随机休息

            # 更新driver页面数据到新的页面
            handle = self.__driver.window_handles
            self.__driver.switch_to.window(handle[-1])

            if web_name == '哔哩哔哩':
                # 更新url到现在页面
                video_page_url = self.__driver.current_url
                print(video_page_url)
                bid = video_page_url.split('/')[-2]
                print(bid)
                bids.append(bid)
                # self.__driver.get(video_page_url)
                index += 1

            elif web_name == '今日头条':

                page_text = self.__driver.page_source
                tree = etree.HTML(page_text)
                src_url = 'https:' + tree.xpath('//video/@src')[0]
                print(src_url)

                title = tree.xpath('//h1/@title | //h2/@title | //h3/@title')[0]

                if src_url.find('blob') == -1:
                    # response = requests.get(url=src_url, headers=self.headers)
                    # urllib.request.urlretrieve(src_url, './视频/' + title)
                    # print(title + ".mp4视频文件下载完成！")

                    dic = {
                        'title': title,
                        'url': src_url
                    }
                    urls.append(dic)
                    index += 1

            if index == 3:
                print("视频链接保存完成！")
                self.__driver.close()
                # self.__driver.quit()
                break

            self.__driver.close()
            self.__driver.switch_to.window(handle_main)

        # bids = ['BV1bH4y1Q7RL', 'BV1sh4y1K7n8', 'BV1Cu4y1C7Xm']
        print(bids)
        print(urls)

        if web_name == '哔哩哔哩':
            for bid in bids:
                # BiLiBiLi = BilibiliVideoAudio(bid)
                video_audio_info = self.__get_bilibili_video_audio(bid)

                title = video_audio_info['title']
                video_url = video_audio_info['video_url']
                audio_url = video_audio_info['audio_url']

                # print(video_url)
                # print(audio_url)

                dic = {
                    'title': title,
                    'video_url': video_url,
                    'audio_url': audio_url
                }
                print("dic['title']" + dic['title'])
                print("dic['video_url']" + dic['video_url'])
                print("dic['audio_url']" + dic['audio_url'])
                urls.append(dic)

        return urls

    def __headers(self):
        one_user_agent = self.__get_one_user_agent()
        # print(one_user_agent)
        headers = {'User-Agent': one_user_agent}
        return headers

    def __sanitize_filename(self, filename):
        # 定义不合规字符的正则表达式
        invalid_chars_regex = r'[\"*<>?\\|/:,]'

        # 替换不合规字符为空格
        sanitized_filename = re.sub(invalid_chars_regex, ' ', filename)

        return sanitized_filename

    def jinritoutiao_get_video_data(self, dic):
        url = dic['url']
        filename = dic['title']
        filename = self.__sanitize_filename(filename)
        print(filename, '正在下载......')
        data = requests.get(url=url, headers=self.__headers).content
        # with open('./视频/' + filename + '.mp4', 'wb') as fp:
        with open('./视频/' + filename + '.mp4', 'wb') as fp:
            fp.write(data)
            print(filename, '下载成功')

    def bilibili_get_video_data(self,dic):
        video_url = dic['video_url']
        audio_url = dic['audio_url']
        filename = dic['title']
        print(filename, '正在下载......')
        # 对文件名进行清理，去除不合规字符
        filename = self.__sanitize_filename(filename)

        try:
            # 发送请求下载视频或音频文件
            resp_video = requests.get(video_url, headers=self.__headers()).content
            resp_audio = requests.get(audio_url, headers=self.__headers()).content
            # download_path = os.path.join('download', filename)  # 构造下载路径
            download_path_video = os.path.join('./视频/' + filename + '.mp4')  # 构造下载路径
            download_path_audio = os.path.join('./视频/' + filename + '.mp3')  # 构造下载路径
            with open(download_path_video, mode='wb') as file:  # 下载视频
                file.write(resp_video)
            with open(download_path_audio, mode='wb') as file:  # 下载音频
                file.write(resp_audio)
            print("{:*^30}".format(f"下载完成：{filename}"))
        except Exception as e:
            print(e)

    def download(self,web_name, urls):
        pool = Pool(4)
        if web_name == '哔哩哔哩':
            pool.map(self.bilibili_get_video_data, urls)
        elif web_name == '今日头条':
            pool.map(self.jinritoutiao_get_video_data, urls)
        pool.close()
        pool.join()


# c = get_urls()
# # urls_list = c.fun_url(web='今日头条', keys='乌克兰')
# urls_list = c.fun_url(web='哔哩哔哩', keys='乌克兰')
#
# # download(web='今日头条', urls=urls_list)
# c.download(web='哔哩哔哩', urls=urls_list)
#
# # download_video_audio(video_url, f"{title}.mp4")  # 下载视频
# # download_video_audio(audio_url, f"{title}.mp3")  # 下载音频

crawl = GetUrls()
crawl.main_request('今日头条')
crawl.input_key('今日头条','乌克兰')
handle_main = crawl.current_window()
crawl.video_btn_click('今日头条')
video_list = crawl.video_list('今日头条')
urls = crawl.video_url_list('今日头条', video_list, handle_main)
print(urls)
