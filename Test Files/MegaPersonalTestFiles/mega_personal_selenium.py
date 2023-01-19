from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime, timedelta


def inputData(name, phone, city, location, desc):
    titled_columns = {
        'name': name,
        'phone-number': phone,
        'city': city,
        'location': location,
        'description': desc
    }

    data = pd.DataFrame(titled_columns)
    data.to_csv('results.csv', index=False, sep="\t")


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get("https://megapersonals.eu")
    assert "Page not found" not in driver.page_source

    # To get the first five - a simple loop. You could add that threading here
    driver.find_element(By.CLASS_NAME, 'btn').click()
    driver.find_element(By.XPATH, '//*[@id="choseCityContainer"]/div[3]/label').click()
    driver.find_element(By.XPATH, '//*[@id="choseCityContainer"]/div[3]/article/div[10]/label').click()
    driver.find_element(By.XPATH, '//*[@id="choseCityContainer"]/div[3]/article/div[10]/article/p[3]/a').click()
    driver.find_element(By.XPATH, '//*[@id="megapCategoriesYellowButton"]/a').click()
    personList = driver.find_elements(By.CLASS_NAME, 'listadd')

    # traverse through list of people to grab page links
    links = []
    for person in personList:
        links.append(person.find_element(By.TAG_NAME, "a").get_attribute("href"))

    # go through each page and grab the data
    print(links)
    counter = 0
    description = []
    name = []
    phoneNumber = []
    city = []
    location = []
    noInfo = "None"
    for link in links:
        driver.get(link)
        # time.sleep(3)
        print(driver.find_element(By.XPATH, "/html/body/div/div[6]").text)

        # check if all these elements exists

        try:
            description.append(driver.find_element(By.XPATH, '/html/body/div/div[6]/span').text)
        except:
            description.append(noInfo)

        try:
            phoneNumber.append(driver.find_element(By.XPATH, '/html/body/div/div[6]/div[1]/span').text)
        except:
            phoneNumber.append(noInfo)

        try:
            name.append(driver.find_element(By.XPATH, '/html/body/div/div[6]/p[1]/span[2]').text[5:])
        except:
            name.append(noInfo)

        try:
            city.append(driver.find_element(By.XPATH, '/html/body/div/div[6]/p[1]/span[1]').text[5:])
        except:
            city.append(noInfo)

        try:
            location.append(driver.find_element(By.XPATH, '/html/body/div/div[6]/p[2]').text[9:])
        except:
            location.append(noInfo)

            # /
        # screenshots
        screenshotName = str(counter) + ".png"
        # schreenShotName = str(datetime.today() - timedelta(days=1)) + str(counter) + ".png"
        # print(schreenShotName.replace(" ", ""))
        driver.save_screenshot(f'screenshots/{screenshotName}')
        counter += 1

    inputData(name, phoneNumber, city, location, description)