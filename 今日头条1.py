# 今日头条搜索框搜索后视频爬取下载

from time import sleep
import random
import requests
import urllib.request
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

s = Service('./chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.get('https://www.toutiao.com/')
sleep(2)

# driver.implicitly_wait(5)

# 搜索框搜索.....
search_input = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div/div[1]/input')
search_input.send_keys('乌克兰')

# 搜索按钮点击
btn = driver.find_element(By.XPATH, value='//*[@id="root"]/div/div[4]/div/div[1]/button')
btn.click()
sleep(2)
# print(search_input)

# 更新driver页面数据到新的页面
handle=driver.window_handles
driver.switch_to.window(handle[-1])

# 更新url到现在页面
# url = driver.current_url
# driver.get(url)
# print(url)
sleep(2)
handle_main = driver.current_window_handle  # 句柄

# page_text = driver.page_source
# with open('./军事/源码.html', 'w', encoding='utf-8') as fp:
#     fp.write(page_text)
# # print(page_text)

# 点击”视频”按钮
video_btn = driver.find_element(By.XPATH, value='//*[@class="cs-view cs-view-flex align-items-center flex-row"]/a[3]')
video_btn.click()
sleep(2)

# 所有视频列表
video_list = driver.find_elements(By.XPATH, value='//*[@class="cs-view cs-view-block cs-grid-cell grid-cell-3 grid-cell-x-m grid-cell-y-m"]/div/div/div[1]')
# video_list = driver.find_elements(By.XPATH, value='//*[@class="cs-view cs-view-block cs-grid-cell grid-cell-3 grid-cell-x-m grid-cell-y-m"//@href')
index = 0
for video in video_list:
    video.click()

    a = random.random() * 3
    sleep(a)  # 设置随机休息

    # 更新driver页面数据到新的页面
    handle=driver.window_handles
    driver.switch_to.window(handle[-1])

    # 更新url到现在页面
    # video_page_url = driver.current_url
    # driver.get(video_page_url)

    page_text = driver.page_source
    tree = etree.HTML(page_text)
    src_url = 'https:' + tree.xpath('//video/@src')[0]
    print(src_url)

    title = tree.xpath('//h1/@title')[0]
    
    if src_url.find('blob') == -1:
        response = requests.get(url=src_url, headers=headers)
        urllib.request.urlretrieve(src_url, './视频/' + title +".mp4")
        print(title + "视频下载完成！")
        index += 1

    if index == 3:
        driver.close()
        print("视频下载完成！")
        break

    driver.close()
    driver.switch_to.window(handle_main)
