import json


class Keywords:
    def __init__(self):
        self.keywords = []
        self.sets = {}

    @staticmethod
    def add_keywords(keyword):
        with open("../keywords.txt", "r+") as filename:
            contentSet = filename.read().splitlines()
            if keyword not in contentSet:
                filename.write("\n" + keyword.lower())
            else:
                print("Keyword already in file")

    @staticmethod
    def remove_keywords(keyword):
        with open("../keywords.txt", "r") as filename:
            contentSet = filename.read().splitlines()
            index = contentSet.index(keyword.lower())

            contentSet.remove(contentSet[index])

        with open("../keywords.txt", "w") as filename:
            filename.write("\n".join(contentSet))

    def create_set(self, setName, keywordsList):
        with open("../keyword_sets.txt", "r") as readfile:
            read = readfile.read()
            if read != '':
                self.sets = json.loads(read)
        self.sets[setName.lower()] = keywordsList.split(', ')
        with open("../keyword_sets.txt", "w") as writefile:
            json.dump(self.sets, writefile)

    def remove_set(self, setName):
        with open("../keyword_sets.txt", "r") as readfile:
            self.sets = json.loads(readfile.read())

        del self.sets[setName.lower()]

        with open('../keyword_sets.txt', 'w') as writefile:
            json.dump(self.sets, writefile)

    def get_keywords(self):
        with open("../keywords.txt", "r") as filename:
            self.keywords = filename.read().splitlines()
        return self.keywords

    def get_set(self):
        with open("../keyword_sets.txt", "r") as filename:
            self.sets = json.loads(filename.read())

        return self.sets

# code to test if the keywords class is working
# if __name__ == '__main__':
#     key = Keywords()
#
#     while True:
#         userInput = input("Type 1 for adding a keyword\n"
#                           "Type 2 for removing a keyword\n"
#                           "Type 3 to add a set\n"
#                           "Type 4 to remove a set\n"
#                           "Type 5 to view keywords\n"
#                           "Type 6 to view sets\n"
#                           "Type 0 to quit\n"
#                           "Enter input: ")
#         if userInput == '1':
#             addWord = input("Type the keyword to add: ")
#             key.add_keywords(addWord)
#         elif userInput == '2':
#             key.get_keywords()
#             removeWord = input("Type keyword to remove: ")
#             key.remove_keywords(removeWord)
#         elif userInput == '3':
#             setKey = input("Enter set name: ")
#             setValues = input("Enter set values seperated by ',': ")
#             key.create_set(setKey, setValues)
#         elif userInput == '4':
#             key.get_set()
#             removeSet = input("Enter set name to remove: ")
#             key.remove_set(removeSet)
#         elif userInput == '5':
#             print(key.get_keywords())
#         elif userInput == '6':
#             print(key.get_set())
#         else:
#             break
