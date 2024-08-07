#!/usr/bin/python
# -*- coding: UTF-8 -*-

from minio import Minio, InvalidResponseError

# 使用endpoint、access key和secret key来初始化minioClient对象。
minioClient = Minio('172.19.0.1:9090',
                    access_key='BqcStXV4CE6hsaqaionQ',
                    secret_key='mF73c5fadQh7EqRSxTFiM2fDEno23qfw2Kci5Auq',
                    secure=False)

try:
    if minioClient.bucket_exists(bucket_name='video'):  # bucket_exists：检查桶是否存在
        print("该存储桶已经存在")
    else:
        minioClient.make_bucket("video")
        print("存储桶创建成功")
except InvalidResponseError as err:
    print(err)