import requests
from urllib.parse import urlencode
from requests import codes
import os
from hashlib import md5
from multiprocessing.pool import Pool


# 首先是获取一页的内容,观察XHR可得知  加载图片是改变offset的值,观察XHR内容得知url和字典内容拼接的字符串为目标网页,判断网页是否响应,如果响应则返回json格式文件,如果不响应则
# 抛出
def get_page(offset):
    params =    {'offset': offset,
     'format': 'json',
     'keyword': '街拍',
     'autoload': 'true',
     'count': '20',
     'cur_tab': '1',
     'from': 'search_tab'

     }
    base_url = 'https://www.toutiao.com/search_content/?'  # 基础网页的基础网址
    url = base_url + urlencode(params)  # 拼接网址
    resp = requests.get(url)
    print(resp.text)
    if resp.status_code == 200:
        return resp.json()



# 第二步,已经获取网页的url,接下来获取想要的内容,已经知道需求是获取妹子图片,通过传入json ,进一步实现获取内
# 容,调取json的方法get(),传入键名字,获取内容
def get_img(json):
    if json.get('data'):  # data是原网页的一个数据集合
        data = json.get('data')
        for item in data:  # 遍历data的内容,
            if item.get('cell_type') is not None:
                continue
            title = item.get('title')
            images = item.get('image_list')
            for image in images:
                yield {
                    'image': 'https:' + image.get('url'),
                    'title': title
                }


# 第三步,保存内容到本地,传入的内容是,获取图片中的item,引入os库用于文件夹操作
def save_files(item):
    img_path = 'img' + os.path.sep +item.get('title')
    if not os.path.exists(img_path):  # 判断文件夹是否存在,如果存在继续,不存在创建继续
        os.makedirs(img_path)
    try:
        resq = requests.get(item.get('image'))
        if resq.status_code == 200:
            file_path = img_path + os.path.sep + '{file_name}.{file_suf}'.format(
                file_name=md5(resq.content).hexdigest(),  # 把获取的内容md5处理获得内容
                file_suf='jpg'
            )
            if not os.path.exists(file_path):
                with open('./test/' + file_path, 'wb') as f:
                    f.write(resq.content)
                    print('Downloaded image path is' + file_path)
            else:
                print('Already Downloaded', file_path)

    except requests.ConnectionError:
        print('Failed to Save Image，item %s' % item)
#第四步 创建运行主函数 main 方法 ,通过offset 数据改变获取内容
def main (offset):
    json = get_page(offset)
    # for item in get_img(json):
    #     save_files(item)

GROUP_START = 0
GROUP_END = 7
#最后调用多线程 进行下载
if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()
    # main

    # https: // so.toutiao.com / search / jump?url = http % 3
    # A % 2
    # F % 2
    # Fwww.toutiao.com % 2
    # Fa7268845376286032424 % 2
    # F % 3
    # Fchannel % 3
    # D % 26
    # source % 3
    # Dvideo & aid = 4916 & jtoken = e5cb68446a79ba5d6b844e3a2da048e73400649db879d5f99655c5543c3686efb99491672718d52b765391178bd887846c721a42f1601823b4220233865c460c