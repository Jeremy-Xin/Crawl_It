import re
import bs4
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class HtmlParser(object):
    '''
    helper class to parse HTML
    '''
    def extract_link(self, text, base_url):
        '''
        extract links from a HTML
        '''
        b_url = urlparse(base_url)
        host = b_url.scheme + '://' + b_url.hostname
        soup = BeautifulSoup(text, 'lxml')
        links = []
        for link in soup.find_all('a'):
            url = str(link.get('href'))
            if url.startswith('/'):
                links.append(urljoin(host, url))
            elif url.startswith('http://') or url.startswith('https://'):
                links.append(url)
        return links
