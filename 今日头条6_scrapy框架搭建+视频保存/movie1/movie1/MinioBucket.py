"""
@Name:test1
@Auth:wu
@Date:2023/12/26
"""
# minio数据库新建桶和上传存储视频
# minio数据库存储视频时同一名称不会重复存储，同一文件不同名称可以重复存储
import os

# 从minio库中导入Minio客户端类
from minio import Minio

# 实例化
client = Minio(
    # endpoint指定的是你Minio的远程IP及端口
    # endpoint="192.168.1.20:9000",http://172.19.0.1/
    endpoint="172.19.0.1:9090",
    # accesskey指定的是你的Minio服务器访问key
    # 默认值为minioadmin
    access_key="BqcStXV4CE6hsaqaionQ",
    # secret_key指定的是你登录时需要用的key，类似密码
    # 默认值也是minioadmin
    secret_key="mF73c5fadQh7EqRSxTFiM2fDEno23qfw2Kci5Auq",
    # secure指定是否以安全模式创建Minio连接
    # 建议为False
    secure=False)
if client.bucket_exists("movie"):
    # 使用with open打开目标文件
    with open("../视频/乌克兰打不动了，转头看向中国，现在是想让中方来“灭火”？.mp4.mp4", "wb") as file_data:
        # 使用os.path.getsize()获取目标文件的大小
        bytes_length = os.path.getsize(
            "../视频/乌克兰打不动了，转头看向中国，现在是想让中方来“灭火”？.mp4.mp4")
else:
    client.make_bucket('movie')
    print("Bucket " + 'movie' + "  maked succeeded")
client.put_object("movie", "乌克兰打不动了，转头看向中国，现在是想让中方来“灭火”？.mp4.mp4", file_data, bytes_length)
