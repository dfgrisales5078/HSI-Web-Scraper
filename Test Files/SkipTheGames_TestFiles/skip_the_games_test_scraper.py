import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging


'''DETECTS BOT & BLOCKS WEBSITE'''

LOG_FILE = 'listings_results.log'
logging.basicConfig(level=logging.INFO,
                    datefmt="%m/%d/%Y %H:%M:%S", filename=LOG_FILE)


class TestScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.location = 'fort-myers'
        self.keywords = ['cash', 'Exotic']
        self.join = ''
        self.payment = ['cash', 'cashapp', 'venmo']
        self.url = f'https://www.skipthegames.com/posts/{self.location}/'
        self.text_search = ''

    def initialize(self):
        self.open_webpage()
        time.sleep(2)
        links = self.get_links()
        time.sleep(5)

        # self.check_post_for_keywords(self.get_data())
        # time.sleep(3)
        # self.capture_screenshot()
        # self.close_webpage()
        # time.sleep(2)
        self.get_data(links)

    def open_webpage(self) -> None:
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        assert "Page not found" not in self.driver.page_source

    def close_webpage(self) -> None:
        self.driver.close()

    def get_links(self):
        posts = self.driver.find_elements(
            By.CSS_SELECTOR, '#gallery_view > div > div > div > div [href]')
        links = [post.get_attribute('href') for post in posts]
        return links[::3]

    def get_data(self, links):
        counter = 0
        for link in links:
            counter += 1

            print(link)
            self.driver.implicitly_wait(10)
            self.driver.get(link)
            assert "Page not found" not in self.driver.page_source
            table = self.driver.find_element(
                By.XPATH, '//*[@id="post-body"]/div/table')
            print(table.text)

            description = self.driver.find_element(
                By.XPATH, '//*[@id="post-body"]')
            print(description.text)
            time.sleep(5)
            print("\n")

            info = table.text + description.text

            for line in info:
                if 'call' in line.lower():
                    print(line)
                    print('keyword found')

            if counter > 6:
                break

    def check_post_for_keywords(self, data):
        for keyword in self.keywords:
            if keyword in data[0] or keyword in data[1]:
                logging.info(data)
            break

    def capture_screenshot(self):
        self.driver.save_screenshot("test_search.png")

    def read_keywords(self) -> str:
        return ' '.join(self.keywords)


if __name__ == "__main__":
    scraper = TestScraper()
    scraper.initialize()
