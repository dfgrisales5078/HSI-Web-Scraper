from Backend.ScraperPrototype import ScraperPrototype
import time
from datetime import datetime
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd
import undetected_chromedriver as uc

class ErosScraper(ScraperPrototype):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.location = 'naples'
        self.url = f'https://www.eros.com/florida/{self.location}/eros.htm'

        # lists to store data and then send to csv file
        self.link = []
        self.profile_header = []
        self.about_info = []
        self.info_details = []
        self.contact_details = []

        # TODO other info needs to be pulled using regex?

    def initialize(self):
        options = uc.ChromeOptions()
        options.headless = False
        self.driver = uc.Chrome(use_subprocess=True, options=options)
        self.open_webpage()
        time.sleep(5)
        links = self.get_links()
        self.get_data(links)
        self.close_webpage()
        self.format_data_to_csv()

    def open_webpage(self) -> None:
        self.driver.get(self.url)
        assert "Page not found" not in self.driver.page_source
        self.driver.maximize_window()

    def close_webpage(self) -> None:
        self.driver.close()

    # TODO - update code to get links from all posts instead
    def get_links(self):
        self.driver.find_element(
            By.XPATH, '//*[@id="agree_enter_website"]').click()
        self.driver.find_element(
            By.XPATH, '// *[ @ id = "ageModal"] / div / div / div[2] / button').click()

        posts = self.driver.find_elements(
            By.CSS_SELECTOR, 'body > div.mainContentWrap > div.container.mainContent > '
                             'div.grid.fourPerRow.mobile.switchable [href]')
        links = [post.get_attribute('href') for post in posts]
        print(set(links))
        return set(links)

    # TODO - change if location changes?
    def get_formatted_url(self):
        pass

    def get_data(self, links):

        self.link = list(links)

        counter = 0
        for link in links:
            print(link)
            self.driver.implicitly_wait(10)
            time.sleep(2)
            self.driver.get(link)
            assert "Page not found" not in self.driver.page_source

            try:
                profile_header = self.driver.find_element(
                    By.XPATH, '//*[@id="pageone"]/div[1]')
                print(profile_header.text)
                self.profile_header.append(profile_header.text)
            except NoSuchElementException:
                self.profile_header.append('none')

            try:
                about_info = self.driver.find_element(
                    By.XPATH, '// *[ @ id = "pageone"] / div[3] / div / div[1] / div[2]')
                print(about_info.text)
                self.about_info.append(about_info.text)
            except NoSuchElementException:
                self.about_info.append('none')

            try:
                info_details = self.driver.find_element(
                    By.XPATH, '//*[@id="pageone"]/div[3]/div/div[2]/div[1]/div')
                print(info_details.text)
                self.info_details.append(info_details.text)
            except NoSuchElementException:
                self.info_details.append('none')

            try:
                contact_details = self.driver.find_element(
                    By.XPATH, '//*[@id="pageone"]/div[3]/div/div[2]/div[2]')
                print(contact_details.text)
                self.contact_details.append(contact_details.text)
            except NoSuchElementException:
                self.contact_details.append('none')

            screenshot_name = str(counter) + ".png"
            self.capture_screenshot(screenshot_name)
            counter += 1

            # if counter > 1:
            #     break

    # TODO - move to class than handles data
    def format_data_to_csv(self):
        titled_columns = {
            'link': self.link,
            'profile_header': self.profile_header,
            'about_info': self.about_info,
            'info_details': self.info_details,
            'contact_details': self.contact_details
        }

        data = pd.DataFrame(titled_columns)
        data.to_csv(f'eros-{str(datetime.today())[0:10]}.csv', index=False, sep='\t')

    def capture_screenshot(self, screenshot_name):
        self.driver.save_screenshot(f'screenshots/{screenshot_name}')

    # TODO - read keywords from keywords.txt
    def read_keywords(self) -> str:
        return ' '.join(self.keywords)