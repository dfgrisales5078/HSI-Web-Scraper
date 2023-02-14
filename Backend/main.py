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
            print(facade.get_escortalligator_cities())
            userInput = input("Select city: ")
            facade.set_escortalligator_city(userInput)
            facade.initialize_escortalligator_scraper(keywordSearchList)
            break

        if website_selection == '2':
            print(facade.get_megapersonals_cities())
            userInput = input("Select city: ")
            facade.set_megapersonals_city(userInput)
            facade.initialize_megapersonals_scraper(keywordSearchList)
            break

        if website_selection == '3':
            print(facade.get_skipthegames_cities())
            userInput = input("Select city: ")
            facade.set_skipthegames_city(userInput)
            facade.initialize_skipthegames_scraper(keywordSearchList)
            break

        if website_selection == '4':
            print(facade.get_yesbackpage_cities())
            userInput = input("Select city: ")
            facade.set_yesbackpage_city(userInput)
            facade.initialize_yesbackpage_scraper(keywordSearchList)
            break

        if website_selection == '5':
            print(facade.get_eros_cities())
            userInput = input("Select city: ")
            facade.set_eros_city(userInput)
            facade.initialize_eros_scraper(keywordSearchList)
            break

