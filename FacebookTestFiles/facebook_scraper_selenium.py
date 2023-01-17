import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
from selenium.webdriver.common.keys import Keys

"""REQUIRES ACCOUNT AFTER A FEW SEARCHES"""


LOG_FILE = 'listings_results.log'
logging.basicConfig(level=logging.INFO,
                    datefmt="%m/%d/%Y %H:%M:%S", filename=LOG_FILE)


class TestScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.location = 'fort-myers'
        self.keywords = ['cashapp']
        self.join = ''
        self.payment = ['cash', 'cashapp', 'venmo']
        self.url = 'https://www.facebook.com/marketplace/fort-myers-fl'
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

    def formatted_url(self):
        return f'https://www.facebook.com/marketplace/fort-myers-fl/search?query={self.keywords[0]}'

    def open_webpage(self) -> None:
        self.driver.implicitly_wait(10)
        self.driver.get(self.formatted_url())
        assert "Page not found" not in self.driver.page_source

    def close_webpage(self) -> None:
        self.driver.close()

    def get_data(self):

        # find & click on first post
        posts = self.driver.find_element(
            By.XPATH, '//*[@id="mount_0_0_OX"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div['
                      '3]/div[1]/div[2]/div[1]/div/div/span/div/div/a/div/div[1]/div/div/div/div/div/img')
        posts.click()

        # get first post data
        post_data = self.driver.find_element(
            By.XPATH, '//*[@id="mount_0_0_OX"]/div/div[1]/div/div[5]/div/div/div[3]/div[2]/div/div[2]/div/div['
                      '2]/div/div[1]')
        print('description data: ', post_data.text)

        time.sleep(7)

        # find and click button to go onto next post
        next_btn = self.driver.find_element(
            By.XPATH, '//*[@id="post-container"]/div/div[3]/div/div/ul/li[2]/a')
        time.sleep(2)

        for i in range(5):
            # find & click on next post button
            next_btn.click()

            # get data of next post
            post_data = self.driver.find_element(
                By.XPATH, '//*[@id="mount_0_0_OX"]/div/div[1]/div/div[5]/div/div/div[3]/div[2]/div/div[2]/div/div['
                          '2]/div/div[1]')
            print('description data: ', post_data.text)

            time.sleep(5)

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
