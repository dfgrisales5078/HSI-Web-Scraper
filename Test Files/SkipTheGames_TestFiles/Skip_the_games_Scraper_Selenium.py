import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
from selenium.webdriver.common.keys import Keys

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
        time.sleep(6)
        self.get_data()
        time.sleep(5)

        # self.check_post_for_keywords(self.get_data())
        # time.sleep(3)
        # self.capture_screenshot()
        # self.close_webpage()
        # time.sleep(2)

    def open_webpage(self) -> None:
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        assert "Page not found" not in self.driver.page_source

    def close_webpage(self) -> None:
        self.driver.close()

    def get_data(self):

        # find & click on first post
        posts = self.driver.find_element(
            By.XPATH, '//*[@id="gallery_view"]/div/div/div/div/a[1]/img')
        posts.click()

        # get first post table & description data
        table_data = self.driver.find_element(
            By.XPATH, '//*[@id="post-body"]/div/table_data')
        print('table data: ', table_data.text)

        description_data = self.driver.find_element(
            By.XPATH, '//*[@id="post-body"]')
        print('description data: ',description_data.text)

        time.sleep(7)

        # scroll down
        html = self.driver.find_element('html')
        html.send_keys(Keys.END)

        # click next button and post table & description data from next listing
        # for i in range(5):
        #     # find & click on next post button
        #     next_btn = self.driver.find_element(
        #         By.XPATH, '//*[@id="post-container"]/div/div[3]/div/div/ul/li[2]/a')
        #     next_btn.click()
        #     time.sleep(2)
        #
        #     # get first post table & description data
        #     table_data = self.driver.find_element(
        #         By.XPATH, '//*[@id="post-body"]/div/table_data')
        #     print('table data: ', table_data.text)
        #
        #     description_data = self.driver.find_element(
        #         By.XPATH, '//*[@id="post-body"]')
        #     print('description data: ', description_data.text)
        #
        #     time.sleep(5)
        #
        #     break

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
