import random
import time

import requests
from bs4 import BeautifulSoup
import re
import json
import hashlib

from config import crawler_conf
from prompt_getter.cleaner.singel_filter import main_filter

class Crawler:
    @classmethod
    def __init__(cls):
        cls.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53',
        }

    @classmethod
    def get_html(cls, url):
        r = requests.get(url, headers=cls.headers)
        r.encoding = r.apparent_encoding
        return r.text

    @classmethod
    def get_uid_list(cls, search_html):
        html = BeautifulSoup(search_html, 'lxml')
        uid_links = html.find_all(name='a', attrs={"class": "bili-video-card__info--owner"})
        uid_list = re.findall(r'<a.*?href="//space.bilibili.com/(\d+)"', ''.join(str(link) for link in uid_links))
        print("uid_list: ", uid_list)
        return list(set(uid_list))

    @classmethod
    def get_aid_list(cls, aid_html):
        results = json.loads(aid_html)
        vlist = results['data']['list']['vlist']
        aid_list = []
        for v in vlist:
            aid = v['aid']
            aid_list.append(aid)
        print('已获得视频数量为：', len(aid_list))
        return aid_list

    @classmethod
    def request_api(cls, url):
        r = requests.get(url, headers=cls.kv)
        r.encoding = r.apparent_encoding
        return r.json()

    @classmethod
    def get_comments(cls, comment_api):
        comment_data = requests.get(comment_api).json()['data']
        reply_list = list(comment_data['replies'])
        return reply_list

    @classmethod
    def save_comments(cls, reply_list, uid):
        m2 = hashlib.md5()
        m2.update(uid.encode('utf-8'))
        with open(f'{crawler_conf["save_path"]}comment_{cls.keyword}_{m2.hexdigest()}.jsonl', 'a+', encoding='utf-8') as f:
            for reply in reply_list:
                # 判断该评论是否存在回复
                if reply['replies'] is None:
                    continue
                comment_text = main_filter(reply['content']['message'])
                reply_text = main_filter(reply['replies'][0]['content']['message'])
                # 判断过滤后是否能够形成对话
                if len(comment_text) == 0 or len(reply_text) == 0:
                    continue
                # 写入文件
                print(comment_text, ' >>>>>> ', reply_text)
                f.write(f'{json.dumps([comment_text, reply_text], ensure_ascii=False)}\n')
            f.close()

    @classmethod
    def run(cls, keyword):
        cls.keyword = keyword
        search_url = f"https://search.bilibili.com/all?keyword={keyword}"
        search_html = cls.get_html(search_url)
        uid_list = cls.get_uid_list(search_html)
        for uid in uid_list:
            aid_url = f"https://api.bilibili.com/x/space/arc/search?mid={uid}&ps=30&tid=0&pn=1&keyword=&order=pubdate&jsonp=jsonp"
            aid_html = cls.get_html(aid_url)
            aid_list = cls.get_aid_list(aid_html)
            # 获取并保存评论
            for aid in aid_list:
                page = 1
                while True:
                    # comment_api = f"https://api.bilibili.com/x/v2/reply?type=1&oid={aid_list[j]}&pn=1"
                    comment_api = f'https://api.bilibili.com/x/v2/reply/main?type=1&oid={aid}&next={page}'
                    reply_list = cls.get_comments(comment_api)
                    if len(reply_list) == 0:
                        break
                    page += 1
                    cls.save_comments(reply_list, uid)
                    time.sleep(random.randint(0, 1))

def main():
    crawler = Crawler()
    for keyword in crawler_conf['keywords']:
        crawler.run(keyword)

if __name__ == '__main__':
    main()

