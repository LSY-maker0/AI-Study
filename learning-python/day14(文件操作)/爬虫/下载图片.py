"""
下载图片 - 下载图片

https://image.so.com/zjl?sn=30&ch=wallpaper

Author: lsy
Date: 2026/1/6
"""
import os
import shutil

import requests

def download_picture(path,url):
    filename=url[url.rfind('/')+1:]
    resp=requests.get(url)
    with open(f'{path}/{filename}', 'wb') as f:
        f.write(resp.content)

def main():
    if not os.path.exists('../resources/images'):
        os.mkdir('../resources/images')
    resp = requests.get('https://image.so.com/zjl?sn=30&ch=wallpaper')
    data = resp.json()['list']
    for item in data:
        picture_url = item['qhimg_url']
        # print(picture_url)
        download_picture('../resources/images', picture_url)

if __name__ == '__main__':
    main()

