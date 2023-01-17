from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from itertools import chain, groupby
import time
import pandas as pd


class MegaPersonalScraper:
    def __init__(self):
        self.driver = webdriver.Firefox()

    def initialize(self):
        self.open_webpage()
        links = self.get_data()
        data = self.formatData(links)
        self.inputToCSV(data['name'], data['phoneNumber'], data['city'], data['location'],
                        data['description'])
        self.close_webpage()

    def open_webpage(self):
        # TODO: make the browser select by location
        self.driver.get('https://megapersonals.eu')
        assert "Page not found" not in self.driver.page_source

    def close_webpage(self):
        self.driver.close()

    def get_formatted_url(self):
        pass

    def get_data(self):
        self.driver.get("https://megapersonals.eu")
        assert "Page not found" not in self.driver.page_source

        # To get the first five - a simple loop. You could add that threading here
        self.driver.find_element(By.CLASS_NAME, 'btn').click()
        self.driver.find_element(By.XPATH, '//*[@id="choseCityContainer"]/div[3]/label').click()
        self.driver.find_element(By.XPATH, '//*[@id="choseCityContainer"]/div[3]/article/div[10]/label').click()
        self.driver.find_element(By.XPATH,
                                 '//*[@id="choseCityContainer"]/div[3]/article/div[10]/article/p[3]/a').click()
        self.driver.find_element(By.XPATH, '//*[@id="megapCategoriesYellowButton"]/a').click()
        personList = self.driver.find_elements(By.CLASS_NAME, 'listadd')

        # traverse through list of people to grab page links
        links = []
        for person in personList:
            links.append(person.find_element(By.TAG_NAME, "a").get_attribute("href"))

        return links

    def formatData(self, links):
        counter = 0
        description = []
        name = []
        phoneNumber = []
        city = []
        location = []
        noInfo = "None"
        for link in links:
            self.driver.get(link)

            # check if all these elements exists
            try:
                description.append(self.driver.find_element(By.XPATH, '/html/body/div/div[6]/span').text)
            except:
                description.append(noInfo)

            try:
                phoneNumber.append(self.driver.find_element(By.XPATH, '/html/body/div/div[6]/div[1]/span').text)
            except:
                phoneNumber.append(noInfo)

            try:
                name.append(self.driver.find_element(By.XPATH, '/html/body/div/div[6]/p[1]/span[2]').text[5:])
            except:
                name.append(noInfo)

            try:
                city.append(self.driver.find_element(By.XPATH, '/html/body/div/div[6]/p[1]/span[1]').text[5:])
            except:
                city.append(noInfo)

            try:
                location.append(self.driver.find_element(By.XPATH, '/html/body/div/div[6]/p[2]').text[9:])
            except:
                location.append(noInfo)

            self.capture_screenshot(counter)
            counter += 1
        return {
            'name': name,
            'phoneNumber': phoneNumber,
            'city': city,
            'location': location,
            'description': description
        }

    def capture_screenshot(self, counter):
        screenshotName = str(counter) + ".png"
        self.driver.save_screenshot(f'screenshots/{screenshotName}')

    def inputToCSV(self, name, phone, city, location, desc):
        titled_columns = {
            'name': name,
            'phone-number': phone,
            'city': city,
            'location': location,
            'description': desc
        }

        data = pd.DataFrame(titled_columns)
        data.to_csv('results.csv', index=False, sep="\t")

    def read_keywords(self):
        pass


if __name__ == '__main__':
    mega_personal = MegaPersonalScraper()
    mega_personal.initialize()
