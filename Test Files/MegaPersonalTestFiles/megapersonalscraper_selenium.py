import time
from datetime import datetime
from selenium.common import NoSuchElementException
import logging
from selenium.webdriver.common.by import By
import pandas as pd
from selenium import webdriver


class TestScraper:
    def __init__(self):
        self.driver = None
        self.location = 'fort-myers'
        self.keywords = ['cash', 'Exotic']
        self.join = ''
        self.payment = ['cash', 'cashapp', 'venmo']
        self.url = "https://megapersonals.eu"
        self.text_search = ''

        # lists to store data and then send to csv file
        self.description = []
        self.name = []
        self.phoneNumber = []
        self.city = []
        self.location = []
        self.link = []

    def initialize(self):
        self.driver = webdriver.Firefox()
        self.open_webpage()

        links = self.get_links()
        self.get_data(links)
        self.format_data_to_csv()
        self.close_webpage()

        # self.check_post_for_keywords(self.get_data())

    def open_webpage(self) -> None:
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        assert "Page not found" not in self.driver.page_source
        # To get the first five - a simple loop. You could add that threading here
        self.driver.find_element(By.CLASS_NAME, 'btn').click()
        self.driver.find_element(By.XPATH, '//*[@id="choseCityContainer"]/div[3]/label').click()
        self.driver.find_element(By.XPATH, '//*[@id="choseCityContainer"]/div[3]/article/div[10]/label').click()
        self.driver.find_element(By.XPATH, '//*[@id="choseCityContainer"]/div[3]/article/div[10]/article/p[3]/a').click()
        self.driver.find_element(By.XPATH, '//*[@id="megapCategoriesOrangeButton"]').click()

    def close_webpage(self) -> None:
        self.driver.close()

    def get_links(self):
        post_list = self.driver.find_elements(By.CLASS_NAME, 'listadd')

        # traverse through list of people to grab page links
        links = []
        for person in post_list:
            links.append(person.find_element(By.TAG_NAME, "a").get_attribute("href"))
        return links

    def get_data(self, links):
        links = set(links)
        counter = 0

        for link in links:
            # append link to list
            self.link.append(link)
            print(link)

            # self.driver.implicitly_wait(2)
            # time.sleep(1)
            self.driver.get(link)
            assert "Page not found" not in self.driver.page_source

            try:
                description = self.driver.find_element(
                    By.XPATH, '/html/body/div/div[6]/span').text
                self.description.append(description)
                print(description)
            except NoSuchElementException:
                self.description.append('N/A')

            try:
                phone_number = self.driver.find_element(
                    By.XPATH, '/html/body/div/div[6]/div[1]/span').text
                self.phoneNumber.append(phone_number)
                print(phone_number)
            except NoSuchElementException:
                self.phoneNumber.append('N/A')

            try:
                name = self.driver.find_element(
                    By.XPATH, '/html/body/div/div[6]/p[1]/span[2]').text[5:]
                self.name.append(name)
                print(name)
            except NoSuchElementException:
                self.name.append('N/A')

            try:
                city = self.driver.find_element(
                    By.XPATH, '/html/body/div/div[6]/p[1]/span[1]').text[5:]
                self.city.append(city)
                print(city)
            except NoSuchElementException:
                self.city.append('N/A')

            try:
                location = self.driver.find_element(
                    By.XPATH, '/html/body/div/div[6]/p[2]').text[9:]
                self.location.append(location)
                print(location)
            except NoSuchElementException:
                self.location.append('N/A')

            # for line in info:
            #     if 'call' in line.lower():
            #         print(line)
            #         print('keyword found')

            screenshot_name = str(counter) + ".png"
            self.capture_screenshot(screenshot_name)
            counter += 1

            # if counter > 15:
            #     break

            print('\n')

    def format_data_to_csv(self):
        titled_columns = {
            'name': self.name,
            'phone-number': self.phoneNumber,
            'city': self.city,
            'location': self.location,
            'description': self.description
        }

        data = pd.DataFrame(titled_columns)
        data.to_csv(f'megapersonals-{str(datetime.today())[0:10]}.csv', index=False, sep="\t")

    # TODO
    def check_post_for_keywords(self, data):
        for keyword in self.keywords:
            if keyword in data[0] or keyword in data[1]:
                logging.info(data)
            break

    def capture_screenshot(self, screenshot_name):
        self.driver.save_screenshot(f'screenshots/{screenshot_name}')

    def read_keywords(self) -> str:
        return ' '.join(self.keywords)


if __name__ == "__main__":
    scraper = TestScraper()
    scraper.initialize()
