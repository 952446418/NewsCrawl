"""
@Name:test.py
@Auth:wu
@Date:2023/12/26
"""
from minio import Minio
from minio.error import InvalidResponseError
import os
import argparse

#执行时 python .\upload2minio.py --host 192.168.18.26:9000 -ak root -sk qweasdzxc -bn movie  -tv abc -tout E:\\temp
parser = argparse.ArgumentParser(description='argparse')
parser.add_argument('--host', '-host', type=str,
                    default="192.168.18.26:9000", required=True, help="minio host")
parser.add_argument('--access_key', '-ak', type=str,
                    default="root", required=True, help="minio access_key")
parser.add_argument('--secret_key', '-sk', type=str,
                    default="qweasdzxc", required=True, help="minio secret_key")
parser.add_argument('--bucket_name', '-bn', type=str,
                    default="movie", required=True, help="minio bucket name")
parser.add_argument('--train_name_and_version', '-tv', type=str,
                    default="", required=True, help="train name and version")
parser.add_argument('--train_out_url', '-tout', type=str,
                    default="", required=True, help="")

args = parser.parse_args()
print('host:'+args.host)
print('ak:'+args.access_key)
print('sk:'+args.secret_key)
print('bucket_name:'+args.bucket_name)
print('train_name_and_version:'+args.train_name_and_version)
print('train_out_url:'+args.train_out_url)

# 从参数取值并赋值给变量
endpoint = args.host
ak = args.access_key
sk = args.secret_key
bucket_name = args.bucket_name
# 以训练名称和版本号组合作为桶下边的第一层文件夹
train_name_and_version = args.train_name_and_version
# 要下载文件夹的根目录
train_out_url = args.train_out_url

# Initialize MinIO client
try:
    client = Minio(endpoint, access_key=ak, secret_key=sk, secure=False)
    print("minio client connected")
except:
    print("minio client init failed")

# 创建桶
try:
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
        print("Bucket " + bucket_name + "  maked succeeded")
    else:
        print("Bucket " + bucket_name + " already exists")
except InvalidResponseError as err:
    print("bucket_exists exception:")
    print(err)

print("train_out_url:"+train_out_url)

print('---------------开始上传minio----------------------')
i=0
try:
    for root, dirs, files in os.walk(train_out_url):
        for file in files:
            i=i+1
            try:
                local_file = os.path.join(root, file)
                print("待上传文件:"+local_file)
                minio_file_path = local_file.replace(
                    train_out_url, train_name_and_version)
                minio_file_path = minio_file_path.replace('\\', '/')
                client.fput_object(bucket_name, minio_file_path, local_file)
                print('已上传文件'+minio_file_path)
            except InvalidResponseError as err:
                print(err)
    print("上传文件结束,共 "+ str(i) +"个文件")
except Exception as ex:
    print("上传minio异常")
    print(ex)
