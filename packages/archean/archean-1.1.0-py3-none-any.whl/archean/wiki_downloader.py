from bs4.element import ResultSet
from bs4 import BeautifulSoup
import requests
import sys
import os


class WikiDumpDownloader():

    def __init__(self, dir:str, base:str = 'https://dumps.wikimedia.org', url:str = 'https://dumps.wikimedia.org/enwiki/') -> None:
        '''
        Wikipedia dump downloader for current page version (including Articles, templates, media/file descriptions, and primary meta-pages) in multiple bz2 streams(100 pages per stream)

            Parameters:
                base : str     Base URL to wikipedia dumps
                url  : str     URL to language-based wikipedia dumps
                dir  : str     Wikipedia dump directory  (example '20170701')

            Returns:
                None
        '''
        self.DOWNLOAD_URL = url
        self.BASE_URL = base
        self.DUMP_DIRECTORY = dir

    def __str__(self) -> str:
        print('WikiDumpDownloader')


    def get_page(self):
        '''
        Fetch the webpage of the DUMP_DIRECTORY
        '''
        # Retrieve the html
        try:
            dump_html = requests.get(self.DOWNLOAD_URL + self.DUMP_DIRECTORY).text
        except requests.exceptions.ConnectionError as e:
            print(e)
            return
        return dump_html


    def parse_latest_links(self, page) -> list:
        '''
        Parse the webpage of the dumps directory to look out for the multistream, current version dumps
        '''
        # Convert to a soup
        if page is None:
            return
        soup_dump = BeautifulSoup(page, 'html.parser')
        # Find list/'li' elements with the class 'done'. In webpage, each section is a list element with class 'done'
        try:
            section = soup_dump.find_all('li', {'class': 'done'})[1]
        except IndexError as e:
            return None
        # Inside section 1(for multistream current version), find all 'li' elements which have anchor tags
        lists:ResultSet = section.find_all('li', {'class': 'file'})
        links = []
        for item in lists:
            a = item.find('a')
            links.append(self.BASE_URL + a.get('href'))
        return links


    def __download__(self, url, filename):
        '''
        Download and display the status of download as a progress bar
        '''
        with open(filename, 'wb') as f:
            response = requests.get(url, stream=True)
            total = response.headers.get('content-length')

            if total is None:
                f.write(response.content)
            else:
                downloaded = 0
                total = int(total)
                for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                    downloaded += len(data)
                    f.write(data)
                    done = int(50*downloaded/total)
                    sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
                    sys.stdout.flush()
        sys.stdout.write('\n')


    def fetch_dumps(self):
        '''
        Fetch the dumps from the wikipedia dumps collection
        '''
        page = self.get_page()
        links = self.parse_latest_links(page)
        if links is None or type(links) is not list or len(links) == 0:
            print('Unable to find any link for downloading the dump')
            return
        for i, link in enumerate(links):
            # file = requests.get(link)
            # print(file.content)
            filename  = link.split('/')[-1]
            if not os.path.exists(filename):
                print('Downloading file {0}/{1} : {2} '.format(i+1, len(links), filename))
                self.__download__(link, filename)
