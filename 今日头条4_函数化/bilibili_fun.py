import os
import requests
import json
import re
from bs4 import BeautifulSoup

class BilibiliVideoAudio:
    def __init__(self, bid):
        self.bid = bid
        self.headers = {
            "referer": "https://www.bilibili.com",
            "origin": "https://www.bilibili.com",
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
            'Accept-Encoding': 'identity'
        }

    def get_video_audio(self):
        # 构造视频链接并发送请求获取页面内容
        url = f'https://www.bilibili.com/video/{self.bid}?spm_id_from=333.851.b_7265636f6d6d656e64.6'
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

#     def download_video_audio(self, url, filename):
#         # 对文件名进行清理，去除不合规字符
#         filename = self.sanitize_filename(filename)
#         try:
#             # 发送请求下载视频或音频文件
#             resp = requests.get(url, headers=self.headers).content
#             # download_path = os.path.join('download', filename)  # 构造下载路径
#             download_path = os.path.join(filename)  # 构造下载路径
#             with open(download_path, mode='wb') as file:
#                 file.write(resp)
#             print("{:*^30}".format(f"下载完成：{filename}"))
#         except Exception as e:
#             print(e)
#
#     def sanitize_filename(self, filename):
#         # 定义不合规字符的正则表达式
#         invalid_chars_regex = r'[\"*<>?\\|/:,]'
#
#         # 替换不合规字符为空格
#         sanitized_filename = re.sub(invalid_chars_regex, ' ', filename)
#
#         return sanitized_filename
#
# def main():
#     bids = ["BV1ha4y1H7sx"]  # 视频的bid，可以修改为其他视频的bid
#     for bid in bids:
#         bilibili = BilibiliVideoAudio(bid)
#         video_audio_info = bilibili.get_video_audio()
#
#         title = video_audio_info['title']
#         video_url = video_audio_info['video_url']
#         audio_url = video_audio_info['audio_url']
#
#         print(video_url)
#         print(audio_url)
#
#         bilibili.download_video_audio(video_url, f"{title}.mp4")  # 下载视频
#         bilibili.download_video_audio(audio_url, f"{title}.mp3")  # 下载音频

# main()

