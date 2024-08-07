"""
@Name:MinioObjectBase.py
@Auth:wu
@Date:2023/12/26
"""
# !/usr/bin/python
# -*- coding: UTF-8 -*-


from MinioConfig import minioClient
from minio.error import InvalidResponseError
import os


class Object:

    # 从桶中下载一个对象txt、csv文件都可以
    def load_object(self):
        try:
            data = minioClient.get_object('testfiles', 'long_lat.csv')
            with open('./load_files/long_lat.csv', 'wb') as file_data:
                for d in data.stream(32 * 1024):
                    file_data.write(d)
            print("Sussess")
        except InvalidResponseError as err:
            print(err)

    # 下载一个对象的指定区间的字节数组
    def load_partial_object(self):
        try:
            data = minioClient.get_partial_object('testfiles', '乌克兰到底阵亡多少人？俄罗斯给出准确数字，已消灭38万乌军-今日头条.mp4', 2, 8)
            with open('user_agent_all_ok.txt', 'wb') as file_data:
                for d in data:
                    file_data.write(d)
            print("Sussess")  # 部分出现乱码
        except InvalidResponseError as err:
            print(err)

    # 下载并将文件保存到本地
    def fget_object(self):
        try:
            print(minioClient.fget_object('testfiles', '乌克兰到底阵亡多少人？俄罗斯给出准确数字，已消灭38万乌军-今日头条.mp4', 'user_agent_all_ok.txt'))
        except InvalidResponseError as err:
            print(err)

    # 拷贝对象存储服务上的源对象到一个新对象
    # 注：该API支持的最大文件大小是5GB
    # 可通过copy_conditions参数设置copy条件
    # 经测试copy复制28M的文件需要663ms; 1.8G的压缩包需要53s
    def get_copy_object(self):
        try:
            copy_result = minioClient.copy_object("movie", "乌克兰到底阵亡多少人？俄罗斯给出准确数字，已消灭38万乌军-今日头条.mp4",
                                                  "user_agent_all_ok.txt"
                                                  )
            print(copy_result)
        except InvalidResponseError as err:
            print(err)

    # 添加一个新的对象到对象存储服务
    """
    单个对象的最大大小限制在5TB。put_object在对象大于5MiB时，自动使用multiple parts方式上传。
    这样，当上传失败时，客户端只需要上传未成功的部分即可（类似断点上传）。
    上传的对象使用MD5SUM签名进行完整性验证。
    """

    def upload_object(self):
        # 放置一个具有默认内容类型的文件，成功后将打印服务器计算出的etag标识符
        try:
            with open('user_agent_all_ok.txt', 'rb') as file_data:
                file_stat = os.stat('./picture_files/user_agent_all_ok.txt')
                print(minioClient.put_object('movie', 'user_agent_all_ok.txt',
                                             file_data, file_stat.st_size))
            print("Sussess")
        except InvalidResponseError as err:
            print(err)
        # 放一个文件'application/csv'
        try:
            with open('user_agent_all_ok.txt', 'rb') as file_data:
                file_stat = os.stat('user_agent_all_ok.txt')
                minioClient.put_object('movie', 'user_agent_all_ok.txt', file_data,
                                       file_stat.st_size, content_type='application/csv')
            print("Sussess")
        except InvalidResponseError as err:
            print(err)

    # 通过文件上传到对象中
    def fput_object(self):
        try:
            print(minioClient.fput_object('pictures', '234.jpg', './picture_files/234.jpg'))
            print("Sussess")
        except InvalidResponseError as err:
            print(err)
        try:
            print(minioClient.fput_object('pictures', 'long_lat.csv',
                                          './picture_files/long_lat.csv',
                                          content_type='application/csv'))
            print("Sussess")
        except InvalidResponseError as err:
            print(err)

    # 获取对象的元数据
    def stat_object(self):
        try:
            print(minioClient.stat_object('pictures', '123.txt'))
        except InvalidResponseError as err:
            print(err)

    # 删除对象
    def remove_object(self):
        try:
            minioClient.remove_object('pictures', '234.jpg')
            print("Sussess")
        except InvalidResponseError as err:
            print(err)

    # 删除存储桶中的多个对象
    def remove_objects(self):
        try:
            objects_to_delete = ['123.txt', 'long_lat.csv']
            for del_err in minioClient.remove_objects('testfiles', objects_to_delete):
                print("Deletion Error: {}".format(del_err))
            print("Sussess")
        except InvalidResponseError as err:
            print(err)

    # 删除一个未完整上传的对象
    def remove_incomplete_upload(self):
        try:
            minioClient.remove_incomplete_upload('testfiles', '123.jpg')
            print("Sussess")
        except InvalidResponseError as err:
            print(err)


if __name__ == '__main__':
    Object().remove_incomplete_upload()