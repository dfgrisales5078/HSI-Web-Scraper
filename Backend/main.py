from Backend.Facade import Facade
from Backend.Keywords import Keywords

if __name__ == '__main__':

    while True:
        website_selection = input('Please make a website to search: '
                                  '\npress 1 to scrape escortalligator '
                                  '\npress 2 to scrape megapersonals '
                                  '\npress 3 to scrape skipthegames '
                                  '\npress 4 to scrape yesbackpage'
                                  '\npress 5 to scrape eros'
                                  '\nor press enter to quit.\n'
                                  '\nEnter your selection: ')
        keyword = Keywords()
        print(keyword.get_keywords())
        keyword_search = input("Enter keywords to search for sperated by ',' --> ")
        keywordSearchList = keyword_search.split(", ")

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
            facade.initialize_yesbackpage_scraper(keywordSearchList)
            break

        if website_selection == '5':
            facade.initialize_eros_scraper()
            break

