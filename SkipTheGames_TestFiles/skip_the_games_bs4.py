
import logging
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup

'''Website detects bot'''

LOG_FILE = 'listings_results.log'
logging.basicConfig(level=logging.INFO,
                    datefmt="%m/%d/%Y %H:%M:%S", filename=LOG_FILE)


class TestScraper:
    def __init__(self):
        self.location = 'fort-myers'
        self.keywords = ['cash', 'Exotic']
        self.join = ''
        self.payment = ['cash', 'cashapp', 'venmo']
        self.url = f'https://www.skipthegames.com/posts/{self.location}/'
        self.text_search = ''

    def initialize(self):
        # self.check_post_for_keywords(self.get_data())
        # self.capture_screenshot()

        soup = BeautifulSoup(self.get_data(self.url), 'html.parser')
        print(soup)

    def get_data(self, uri):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
        try:
            response = requests.get(uri, headers=headers)
            response.raise_for_status()
        except HTTPError as httperror:
            print(httperror)
            exit(1)
        except Exception as error:
            print(error)
            exit(1)

        return response.content

    def get_formatted_url(self) -> str:
        return f'https://www.skipthegames.com/posts/{self.location}/"'

    def check_post_for_keywords(self, data):
        for keyword in self.keywords:
            if keyword in data[0] or keyword in data[1]:
                logging.info(data)
            break

    def capture_screenshot(self):
        pass

    def read_keywords(self) -> str:
        return ' '.join(self.keywords)


if __name__ == "__main__":
    scraper = TestScraper()
    scraper.initialize()

