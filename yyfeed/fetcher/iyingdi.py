# -*- coding: utf-8 -*-
import json
import re
from json import JSONDecodeError
from typing import Iterable

from yyutil.time import fromtimestamp
from .base import Fetcher, Item


class IYingDiFetcher(Fetcher):
    BASE_URL = 'https://www.iyingdi.com'

    SOURCE_URL = BASE_URL + '/rstag/get/source?tagId=%d&module=2&system=web'
    ARTICLE_URL = BASE_URL + '/article/%s'

    ARTICLE_LINK_URL = BASE_URL + '/web/article/home/%s'
    BBSPOST_LINK_URL = BASE_URL + '/web/bbspost/detail/%s'
    USER_URL = BASE_URL + '/web/personal/home?id=%d'

    def __init__(self, tag_id=17):
        super().__init__()
        self.article_url = self.SOURCE_URL % tag_id

    def fetch(self) -> Iterable[Item]:
        for e in self.get_data(self.article_url, 'feeds'):
            feed = e['feed']

            sid = feed['sourceID']
            title = feed['title']
            publish_date = fromtimestamp(feed['created'])
            clazz = feed['clazz']

            # noinspection PyUnusedLocal
            link = self.BASE_URL
            description = title

            if clazz == 'article':
                link = self.ARTICLE_LINK_URL % sid

                url = self.ARTICLE_URL % sid
                article = self.get_cached_data(url, 'article')
                description = self.get_content(article, feed.get('description'))

            elif clazz == 'bbsPost':
                link = self.BBSPOST_LINK_URL % sid
                pass

            else:
                continue

            yield Item(sid, title, publish_date, link, description)

        return []

    def get_content(self, article, description):
        texts = []
        if description:
            texts.append('<blockquote>%s</blockquote>' % description)

        running = True
        try:
            article = json.loads(article['content'])
        except JSONDecodeError:
            texts.append(article['content'])
            running = False

        if running:
            for content in article:
                content_type = content['type']
                text = ''

                if content_type == 'text':
                    text = content['content']

                elif content_type in ('image', 'subject-content-headImg'):
                    text = '<img src="%s">' % content['url']
                    caption = content.get('caption')
                    if caption:
                        text += '<br><span>%s</span>' % caption

                elif content_type in ('media', 'video'):
                    text = content.get('content')
                    if not text:
                        text = '<video preload="auto" controls="controls" src="%s" poster="%s"></video>' % (
                            content['url'], content['thumbnail']
                        )

                    caption = content.get('caption')
                    if caption:
                        text += '<br><span>%s</span>' % caption

                elif content_type == 'audio':
                    text = '<audio preload="auto" controls="controls" src="%s"></video>' % (
                        content['src']
                    )

                    title = content['title']
                    if title:
                        title += '<br><span>%s</span>' % title

                elif content_type == 'deckCode':
                    text = '<img src="%s">' % content['deckIcon']
                    code = content.get('code')
                    if code:
                        code = re.sub(r'^[ #]*(.*?)[ #]*$', r'\1', code)
                        text += '<br><blockquote>%s</blockquote>' % code

                elif content_type == 'deckSet':
                    text = '<a href="%s">点击进入套牌集</a>' % content['webDeckSetLink']

                elif content_type == 'insertUser':
                    user = None
                    try:
                        user = json.loads(content['user'])
                    except JSONDecodeError:
                        text = str(content)

                    if user:
                        head = user['head']
                        name = user['username']
                        description = user['description']
                        url = self.USER_URL % user['id']
                        text = '<blockquote><a href="%s"><img src="%s"></a>' \
                               '<span>%s</span>：<span>%s</span></blockquote>' \
                               % (url, head, name, description)

                else:
                    text = str(content)

                text = re.sub(r'wanxiu://innerlink\?type=article_link&amp;id=(\d+)',
                              r'https://www.iyingdi.cn/web/article/search/\1', text)

                texts.append(text)

        return '<div>' + '</div><br>\n<div>'.join(texts) + '</div>'

    def get_data(self, url, key=None):
        data = self.fetcher.json(url)
        if not data.get('success', False):
            msg = data.get('msg', "Cannot get data from IYingDi")
            raise RuntimeError(msg)
        return data[key] if key else data

    def get_cached_data(self, url, key=None):
        cache_id = url + "|" + key if key else url

        data = self.cache.get(cache_id)
        if data is not None:
            return data

        data = self.get_data(url, key)
        if data is not None:
            self.cache[cache_id] = data

        return data
