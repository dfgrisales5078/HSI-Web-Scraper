from Backend.Facade import Facade

if __name__ == '__main__':
    while True:
        website_selection = input('Please make a website to search: '
                                  '\npress 1 to scrape escortalligator '
                                  '\npress 2 to scrape megapersonals '
                                  '\npress 3 to scrape skipthegames '
                                  '\npress 4 to scrape yesbackpage'
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



