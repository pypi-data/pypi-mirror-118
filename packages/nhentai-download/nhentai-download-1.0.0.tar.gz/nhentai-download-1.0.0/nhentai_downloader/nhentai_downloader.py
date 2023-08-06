import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from time import sleep
import threading


class NhentaiDownloader:
    _DOMAIN = 'https://nhentai.net/g/'

    def __init__(self, god_numbers, path='./', filename=''):
        self.god_numbers = god_numbers
        self.path = path
        self.filename = filename

    def download_image(self, url, path):
        if not os.path.isdir(path):
            try:
                os.makedirs(path)
            except FileExistsError:
                pass
        response = requests.get(url=url, stream=True)
        filename = url.split('/')[-1]
        filename = f'{self.filename}{filename}'
        block_size = 1024
        wrote = 0
        with open(f'{path}/{filename}', 'wb') as f:
            for data in tqdm(response.iter_content(block_size), desc=f'{filename}'):
                wrote = wrote + len(data)
                f.write(data)

    @staticmethod
    def get_origin_url(url):
        result = list(url)
        result[url.find('t.nhentai.net')] = 'i'
        f = url.find('t.jpg') if url.find('t.jpg') != -1 else url.find('t.png')
        result[f] = ''
        return ''.join(result)

    def _get_origin_urls(self, thumbs):
        origin_urls = list()
        for thumb in thumbs:
            tumbnail_url = thumb.find_next('img').get('data-src')
            origin_url = self.get_origin_url(url=tumbnail_url)
            origin_urls.append(origin_url)
        return origin_urls

    def _download_images(self, title, origin_urls):
        threads = list()
        path = f'{self.path}/{title}'
        for url in origin_urls:
            thread = threading.Thread(
                target=self.download_image, args=(url, path))
            thread.start()
            threads.append(thread)
            sleep(1)

        for thread in threads:
            thread.join()

    def exec(self):
        for god_number in self.god_numbers:
            html_doc = requests.get(url=f'{self._DOMAIN}{god_number}/').text
            soup = bs(html_doc, 'html.parser')
            title = soup.select_one('h2.title>.pretty').text
            thumbs = soup.find_all('div', {'class': 'thumb-container'})
            origin_urls = self._get_origin_urls(thumbs=thumbs)
            self._download_images(title=title, origin_urls=origin_urls)
