import ast
import json
import pickle


class Keywords:
    def __init__(self):
        self.keywords = None
        self.sets = {}

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
            contentSet = filename.read().splitlines()
            index = contentSet.index(keyword)
            print(contentSet)
            contentSet.remove(contentSet[index])
            print(contentSet)

        with open("keywords.txt", "w") as filename:
            filename.write("\n".join(contentSet))

    def create_set(self, setName, keywordsList):
        with open("keyword_sets.txt", "r") as readfile:
            self.sets = json.loads(readfile.read())
        self.sets[setName] = keywordsList.split(', ')

        with open("keyword_sets.txt", "w") as writefile:
            json.dump(self.sets, writefile)
        return

# {"Testing": ["guru", "hello", "deepa"], "SE": ["guru", "hello", "deepa"], "Doggo": ["guru", "hello", "deepa"]}
    def remove_set(self, setName):
        with open("keyword_sets.txt", "r") as readfile:
            self.sets = json.loads(readfile.read())
            print(self.sets)

        del self.sets[setName]

        with open('keyword_sets.txt', 'w') as writefile:
            json.dump(self.sets, writefile)
        return

    @staticmethod
    def get_keywords(self):
        pass


if __name__ == '__main__':
    key = Keywords()

    while True:
        # keyInput = input("Enter Key word for set: ")
        # words = input("Enter list of keys to add to set seperated by ',': ")
        # key.create_set(keyInput, words)

        removeKey = input("Enter key word to remove: ")
        key.remove_set(removeKey)
        break

