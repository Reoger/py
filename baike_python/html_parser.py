import re
import urlparse

from bs4 import BeautifulSoup

class HtmlParser(object):
    def parse(self, new_url, html_con):
        if new_url is None or html_con is None:
            return
        soup = BeautifulSoup(html_con,'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(new_url,soup)
        new_data = self._get_new_data(new_url,soup)
        return new_urls,new_data

    def _get_new_data(self, page_url, soup):
        res_data = {}

        # url
        res_data['url'] = page_url

        title_node = soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find("h1")
        res_data['title'] = title_node.get_text()
        summary_node = soup.find('div', class_="lemma-summary")
        res_data['summary'] = summary_node.get_text()

        return res_data

    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        links = soup.find_all('a', href=re.compile(r'/item/'))
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls


