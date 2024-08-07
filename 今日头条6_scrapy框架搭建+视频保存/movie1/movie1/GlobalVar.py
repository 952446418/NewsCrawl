# 定义全局变量

import random


def get_one_user_agent():
    with open(
            'E:/个人/代码/爬虫代码/pachong/军事视频代码/jinritoutiao/今日头条5_scrapy框架搭建/movie/user_agent_all_ok.txt',
            'r', encoding='utf-8') as file:
        ret = file.readlines()
    user_agent_list = [i.strip() for i in ret]
    one_user_agent = random.choice(user_agent_list)
    return one_user_agent


# UA伪装
user_agent = get_one_user_agent()

# key