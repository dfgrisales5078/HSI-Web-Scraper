class Keywords:
    def __init__(self):
        self.keywords = None
        self.sets = None

    @staticmethod
    def add_keywords(keyword):
        with open("keywords.txt", "r+") as filename:
            contentSet = filename.read().splitlines()

            if keyword not in contentSet:
                filename.write("\n" + keyword)
            else:
                print("Error")



    @staticmethod
    def remove_keywords(keyword):
        with open("keywords.txt", "r") as filename:
            contentSet = filename.read()
            print(contentSet)
            #if keyword in contentSet:

            #
        with open("keywords.txt", "w") as filename:
            newcontent = contentSet.replace(keyword, "")
            filename.write(newcontent)



            # if keyword in contentSet:
            #     index = contentSet.index(keyword)
            #     contentSet.remove(contentSet[index])
            #
            #     with open("keywords.txt", "w") as writefile:
            #         writefile.write(*contentSet)

            print(contentSet)


    @staticmethod
    def create_set(self):
        pass

    @staticmethod
    def remove_set(self):
        pass

    @staticmethod
    def get_keywords(self):
        pass


if __name__ == '__main__':
    keyword = Keywords()
    data = "incall"
    keyword.add_keywords(data)
    keyword.remove_keywords(data)