from Backend.Facade import Facade
from datetime import datetime
import os

if __name__ == '__main__':

    # date_time = str(datetime.today())[0:19]
    # date_time = date_time.replace(' ', '_')
    # date_time = date_time.replace(':', '-')
    # path = f'yesbackpage_{date_time}'
    # os.mkdir(path)
    # print(path)

    while True:
        website_selection = input('Please make a website to search: '
                                  '\npress 1 to scrape escortalligator '
                                  '\npress 2 to scrape megapersonals '
                                  '\npress 3 to scrape skipthegames '
                                  '\npress 4 to scrape yesbackpage'
                                  '\npress 5 to scrape eros'
                                  '\nor press enter to quit.\n'
                                  '\nEnter your selection: ')

        if website_selection == '':
            exit(0)

        facade = Facade()

        if website_selection == '1':
            facade.initialize_escortalligator_scraper()
            break

        if website_selection == '2':
            facade.initialize_megapersonals_scraper()
            break

        if website_selection == '3':
            facade.initialize_skipthegames_scraper()
            break

        if website_selection == '4':
            facade.initialize_yesbackpage_scraper()
            break

        if website_selection == '5':
            facade.initialize_eros_scraper()
            break

