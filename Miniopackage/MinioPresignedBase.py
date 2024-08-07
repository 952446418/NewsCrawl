"""
@Name:MinioPresignedBase.py
@Auth:wu
@Date:2023/12/26
"""

from MinioConfig import minioClient
from minio.error import InvalidResponseError
from datetime import timedelta


class Presigned:

    # 生成一个用于HTTP GET操作的presigned URL
    def presigned_get_object(self):
        # 预先获得的对象名称的获取对象URL，将在2天后过期
        try:
            print(minioClient.presigned_get_object('testfiles', '乌克兰到底阵亡多少人？俄罗斯给出准确数字，已消灭38万乌军-今日头条.mp4', expires=timedelta(days=7)))
            print("Sussess")
        # 由于内部预定位确实会获得存储桶位置，因此仍然可能出现响应错误
        except InvalidResponseError as err:
            print(err)

    # 生成一个用于HTTP PUT操作的presigned URL
    def presigned_put_object(self):
        try:
            print(minioClient.presigned_put_object('testfiles',
                                                   '乌克兰到底阵亡多少人？俄罗斯给出准确数字，已消灭38万乌军-今日头条.mp4',
                                                   expires=timedelta(days=7)))
            print("Sussess")
        except InvalidResponseError as err:
            print(err)

    # 允许给POST操作的presigned URL设置策略条件。这些策略包括比如，
    # 接收对象上传的存储桶名称，名称前缀，过期策略
    def presigned_post_policy(self, PostPolicy):
        pass


if __name__ == '__main__':
    Presigned().presigned_put_object()