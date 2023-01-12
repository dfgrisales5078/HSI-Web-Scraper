import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestScraper:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.location = 'fort-myers'
        self.keywords = ['outcall', 'independent']
        self.join = ''
        self.payment = ['cash', 'cashapp', 'venmo']
        self.url = 'https://skipthegames.com/posts/'
        self.text_search = ''

    def initialize(self):
        self.open_webpage()
        time.sleep(5)
        self.get_data()
        self.capture_screenshot()
        self.close_webpage()

    def open_webpage(self) -> None:
        self.driver.get(self.get_formatted_url())
        assert "Page not found" not in self.driver.page_source

    def close_webpage(self) -> None:
        self.driver.close()

    def get_formatted_url(self) -> str:
        return f'https://skipthegames.com/posts/{self.location}/?keywords="{self.read_keywords()}"'

    def get_data(self):
        listings = self.driver.find_element(
            By.XPATH, '/html/body/div[9]/table')
        print(listings)
        print(listings.text)

    def capture_screenshot(self):
        self.driver.save_screenshot("test_search.png")

    def read_keywords(self) -> str:
        return ' '.join(self.keywords)


if __name__ == "__main__":
    scraper = TestScraper()
    scraper.initialize()
