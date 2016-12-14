# -*- coding: utf-8 -*-
import json
from typing import Sequence

from yyutil.time import fromtimestamp
from .base import Fetcher, Item


class IYingDiFetcher(Fetcher):
    BASE_URL = 'http://www.iyingdi.com'
    ARTICLE_URL = BASE_URL + "/article"

    MODULE_URL = ARTICLE_URL + '/module/list?version=10000'
    MODULE_BASE_URL = BASE_URL + "/web/articles/%s"

    LIST_URL = ARTICLE_URL + '/list?size=%d&module=%d&version=10000&visible=1'
    DATA_URL = ARTICLE_URL + '/%d'
    ITEM_URL = BASE_URL + '/web/articles/%s/%d'

    def __init__(self, module=12, size=20):
        super().__init__()
        self.article_url = type(self).LIST_URL % (size, module)

        self.module = "top"
        self.module_id = module
        self.module_url = None

    def url(self) -> str:
        if not self.module_url:
            not_find = True
            for e in self.get_data(type(self).MODULE_URL, "modules"):
                if self.module_id == e['id']:
                    self.module = e['oldTitle']
                    self.module_url = type(self).MODULE_BASE_URL % self.module
                    not_find = False
            if not_find:
                raise RuntimeError('unknown id')

        return self.module_url

    def fetch(self) -> Sequence[Item]:
        results = []
        for e in self.get_data(self.article_url, 'articles'):
            uid = e[0]
            url = type(self).DATA_URL % uid
            article = self.get_cached_data(url, 'article')

            publish_date = fromtimestamp(article['created'])
            link = type(self).ITEM_URL % (self.module, uid)

            description = self.get_content(article)

            results.append(Item(uid, article['title'], publish_date, link, description))

        return results

    def get_data(self, url, key):
        data = self.fetcher.json(url)
        if not data.get('success', False):
            msg = data.get('msg', "Cannot get data from IYingDi")
            raise RuntimeError(msg)
        return data[key]

    def get_cached_data(self, url, key):
        cache_id = url + "|" + key

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
        except:
            return article['content']

        for content in article:
            content_type = content['type']

            if content_type == 'text':
                text = content['content']

            elif content_type == 'image':
                text = '<img src="%s">' % content['url']
                caption = content['caption']
                if caption:
                    text += '<br><span>%s</span>' % caption

            elif content_type == "video":
                text = '<video preload="auto" controls="controls" src="%s" poster="%s"></video>' % (
                    content['url'], content['thumbnail']
                )
                caption = content['caption']
                if caption:
                    text += '<br><span>%s</span>' % caption

            else:
                text = str(content)

            texts.append(text)

        return '<div>' + '</div><br>\n<div>'.join(texts) + '</div>'
