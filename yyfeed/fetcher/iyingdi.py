# -*- coding: utf-8 -*-
import json
from json import JSONDecodeError
from typing import Iterable

from yyutil.time import fromtimestamp
from .base import Fetcher, Item


class IYingDiFetcher(Fetcher):
    BASE_URL = 'http://www.iyingdi.com'
    ARTICLE_URL = BASE_URL + "/article"

    MODULE_URL = ARTICLE_URL + '/module/list?version=10000'
    MODULE_BASE_URL = BASE_URL + "/web/articles/%s"

    LIST_URL = ARTICLE_URL + '/list?size=%d&module=%d&version=10000&visible=1'
    DATA_URL = ARTICLE_URL + '/%d'
    TOPICS_URL = DATA_URL + '/topics'
    ITEM_URL = BASE_URL + '/web/articles/%s/%d'

    def __init__(self, module=12, size=100):
        super().__init__()
        self.article_url = self.LIST_URL % (size - 1, module)

        self.module = "top"
        self.module_id = module
        self.module_url = None

    def url(self) -> str:
        if not self.module_url:
            not_find = True
            for e in self.get_data(self.MODULE_URL, "modules"):
                if self.module_id == e['id']:
                    self.module = e['oldTitle']
                    self.module_url = self.MODULE_BASE_URL % self.module
                    not_find = False
            if not_find:
                raise RuntimeError('unknown id')

        return self.module_url

    def fetch(self) -> Iterable[Item]:
        for e in self.get_data(self.article_url, 'articles'):
            uid = e[0]
            url = self.DATA_URL % uid
            article = self.get_cached_data(url, 'article')

            publish_date = fromtimestamp(article['created'])
            link = self.ITEM_URL % (self.module, uid)

            description = self.get_content(article)
            if article.get('typee') == 2:
                description += self.get_topics(uid)

            yield Item(uid, article['title'], publish_date, link, description)

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

    @staticmethod
    def get_content(article):
        texts = []

        try:
            article = json.loads(article['content'])
        except JSONDecodeError:
            return '<div>%s</div>' % article['content']

        for content in article:
            content_type = content['type']

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

            else:
                text = str(content)

            texts.append(text)

        return '<div>' + '</div><br>\n<div>'.join(texts) + '</div>'

    def get_topics(self, uid):
        url = self.TOPICS_URL % uid
        data = self.get_cached_data(url)
        articles = data['articles']

        text = '<div><table><colgroup><col width="30%"><col width="70%"></colgroup><tbody>'
        for topic in data['topic']['remark'].split():
            for item in articles[topic]:
                text += '<tr><td><img width="160" height="90" src="%s"></td>' % item[7]
                text += '<td><a href="%s">%s</a></td></tr>' % (
                    self.ITEM_URL % (self.module, item[0]), item[1]
                )

        text += '</tbody></table></div>'
        return text
