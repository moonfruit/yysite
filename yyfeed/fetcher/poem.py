from datetime import datetime
from typing import Iterable

# noinspection PyProtectedMember
from bs4 import SoupStrainer

from yyfeed.fetcher import Fetcher, Item
from yyutil.time import astimezone


class PoemFetcher(Fetcher):
    URL = 'http://www.thepoemforyou.com/ruheshouting/2018niandebochudan/'
    FILTER = SoupStrainer('table')
    FILTER_CONTENT = SoupStrainer('div', 'post postimg')
    DATE_FORMAT_6 = '%y%m%d'
    DATE_FORMAT_8 = '%Y%m%d'

    def fetch(self) -> Iterable[Item]:
        soup = self.fetcher.soup(self.URL, parse_only=self.FILTER)

        for tr in soup.find_all('tr'):
            tds = tr.find_all('td')

            item_id = tds[0].text
            title = tds[1].text + ' ' + tds[2].text
            date = self.id2date(item_id)
            link = tds[2].a['href']

            yield Item(item_id, title, date, link, "")

    def id2date(self, item_id):
        numbers = []
        for c in item_id:
            if len(numbers) >= 8:
                break
            if '0' <= c <= '9':
                numbers.append(c)
            else:
                break
        numbers = "".join(numbers)
        if len(numbers) >= 8:
            return astimezone(datetime.strptime(numbers[:8], self.DATE_FORMAT_8))
        elif len(numbers) >= 6:
            return astimezone(datetime.strptime(numbers[:6], self.DATE_FORMAT_6))
