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


def get_one_user_agent():
    with open('./user_agent_all_ok.txt', 'r', encoding='utf-8') as file:
        ret = file.readlines()
    user_agent_list = [i.strip() for i in ret]
    one_user_agent = random.choice(user_agent_list)
    return one_user_agent


class get_urls():

    def __init__(self):
        self.one_user_agent = get_one_user_agent()
        # print(one_user_agent)
        self.headers = {'User-Agent': self.one_user_agent}

    def get_video_audio(self, bid):
        # 构造视频链接并发送请求获取页面内容
        url = f'https://www.bilibili.com/video/{bid}?spm_id_from=333.851.b_7265636f6d6d656e64.6'
        content = requests.get(url, headers=self.headers).content.decode('utf-8')
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

    def fun_url(self, web, keys):
        # 随机返回一个user_agent进行UI伪装
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        # }

        web_url = ''
        search_btn_url = ''
        video_list_url = ''
        if web == '今日头条':
            web_url = 'https://www.toutiao.com/'
            search_btn_url = '//*[@id="root"]/div/div[4]/div/div[1]/button'
            video_list_url = '//*[@class="cs-view cs-view-block cs-grid-cell grid-cell-3 grid-cell-x-m grid-cell-y-m"]/div/div/div[1]'

        elif web == '哔哩哔哩':
            web_url = 'https://www.bilibili.com/'
            search_btn_url = '//*[@id="nav-searchform"]/div[2]'
            video_list_url = '//*[@class="video-item matrix"]/a'

        print(web_url)
        print(search_btn_url)

        # one_user_agent = get_one_user_agent()
        # # print(one_user_agent)
        # headers = {'User-Agent': one_user_agent}

        option = webdriver.ChromeOptions()
        # #设置无头模式
        # option.add_argument("--headless")

        # 关闭左上方 Chrome 正受到自动测试软件的控制的提示
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)

        # 设置user-agent
        # option.add_argument('user-agent=' + headers['User-Agent'])
        option.add_argument('user-agent=' + self.one_user_agent)

        # driver = webdriver.Chrome(options=option)
        s = Service('./chromedriver.exe')
        driver = webdriver.Chrome(service=s, options=option)
        # driver = webdriver.Chrome(service=s)

        driver.get(web_url)
        # sleep(2)

        driver.implicitly_wait(2)

        # 主页搜索框搜索.....
        # search_input = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div/div[1]/input')
        search_input = driver.find_element(By.XPATH, '//input')
        search_input.send_keys(keys)

        # 主页搜索按钮点击
        btn = driver.find_element(By.XPATH, value=search_btn_url)
        btn.click()
        # sleep(2)
        driver.implicitly_wait(2)

        # print(search_input)

        # 更新driver页面数据到新的页面（主界面——搜索界面）
        handle = driver.window_handles
        driver.switch_to.window(handle[-1])

        # 更新url到现在页面——搜索界面
        # url = driver.current_url
        # driver.get(url)
        # print(url)
        # sleep(2)
        driver.implicitly_wait(2)

        handle_main = driver.current_window_handle  # 句柄

        # page_text = driver.page_source
        # with open('./军事/源码.html', 'w', encoding='utf-8') as fp:
        #     fp.write(page_text)
        # # print(page_text)

        # 今日头条点击到“视频”界面
        if web == '今日头条':
            video_btn = driver.find_element(By.XPATH,
                                            value='//*[@class="cs-view cs-view-flex align-items-center flex-row"]/a[3]')
            video_btn.click()
            # sleep(2)
            driver.implicitly_wait(2)

        video_list = driver.find_elements(By.XPATH, value=video_list_url)
        # video_list = driver.find_elements(By.XPATH, value='//*[@class="cs-view cs-view-block cs-grid-cell grid-cell-3 grid-cell-x-m grid-cell-y-m"//@href')
        index = 0
        urls = []  # 存储所有视频的链接和文件名
        bids = []

        for video in video_list:
            video.click()
            a = random.random() * 3
            sleep(a)  # 设置随机休息

            # 更新driver页面数据到新的页面
            handle = driver.window_handles
            driver.switch_to.window(handle[-1])

            if web == '哔哩哔哩':
                # 更新url到现在页面
                video_page_url = driver.current_url
                print(video_page_url)
                bid = video_page_url.split('/')[-2]
                print(bid)
                bids.append(bid)
                # driver.get(video_page_url)
                index += 1

            elif web == '今日头条':

                page_text = driver.page_source
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
                driver.close()
                # driver.quit()
                break

            driver.close()
            driver.switch_to.window(handle_main)

        # bids = ['BV1bH4y1Q7RL', 'BV1sh4y1K7n8', 'BV1Cu4y1C7Xm']
        print(bids)
        print(urls)

        if web == '哔哩哔哩':
            for bid in bids:
                # BiLiBiLi = BilibiliVideoAudio(bid)
                video_audio_info = self.get_video_audio(bid)

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





def sanitize_filename(filename):
    # 定义不合规字符的正则表达式
    invalid_chars_regex = r'[\"*<>?\\|/:,]'

    # 替换不合规字符为空格
    sanitized_filename = re.sub(invalid_chars_regex, ' ', filename)

    return sanitized_filename


def jinritoutiao_get_video_data(dic):
    url = dic['url']
    filename = dic['title']
    filename = sanitize_filename(filename)
    print(filename, '正在下载......')
    data = requests.get(url=url, headers=headers()).content
    # with open('./视频/' + filename + '.mp4', 'wb') as fp:
    with open('./视频/' + filename + '.mp4', 'wb') as fp:
        fp.write(data)
        print(filename, '下载成功')


def bilibili_get_video_data(dic):
    video_url = dic['video_url']
    audio_url = dic['audio_url']
    filename = dic['title']
    print(filename, '正在下载......')
    # 对文件名进行清理，去除不合规字符
    filename = sanitize_filename(filename)

    try:
        # 发送请求下载视频或音频文件
        resp_video = requests.get(video_url, headers=headers()).content
        resp_audio = requests.get(audio_url, headers=headers()).content
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


def download(web, urls):
    pool = Pool(4)
    if web == '哔哩哔哩':
        pool.map(bilibili_get_video_data, urls)
    elif web == '今日头条':
        pool.map(jinritoutiao_get_video_data, urls)
    pool.close()
    pool.join()


c = get_urls()
# urls_list = c.fun_url(web='今日头条', keys='乌克兰')
urls_list = c.fun_url(web='哔哩哔哩', keys='乌克兰')

# download(web='今日头条', urls=urls_list)
download(web='哔哩哔哩', urls=urls_list)

# download_video_audio(video_url, f"{title}.mp4")  # 下载视频
# download_video_audio(audio_url, f"{title}.mp3")  # 下载音频
