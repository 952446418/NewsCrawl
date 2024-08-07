# movie1/begin.py
from scrapy import cmdline


# 信息提取类
# cmdline.execute("scrapy crawl movie1 -a key=乌克兰".split())
cmdline.execute("scrapy crawl movie".split())

# # 目标识别类
# import os
# os.environ['KMP_DUPLICATE_LIB_OK']='True'
#
# from ultralytics import YOLO
#
# if __name__ == '__main__':
#     model = YOLO(r'yolov8n.pt',task='segment')
#     dir = r'./视频/乌克兰到底阵亡多少人？俄罗斯给出准确数字，已消灭38万乌军-今日头条.mp4'
#     model.predict(source=dir, save=True, show=True)