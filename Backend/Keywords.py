import json


class Keywords:
    def __init__(self):
        self.keywords = []
        self.sets = {}
        self.keywords_path = ''
        self.keywords_set_path = ''

    def set_keywords_path(self, keyword_file_path):
        self.keywords_path = keyword_file_path

    def set_keywords_sets_path(self, keyword_sets_file_path):
        self.keywords_set_path = keyword_sets_file_path

    def add_keywords(self, keyword):
        # self.keywords.append(keyword)
        if self.keywords_path != '':
            with open(self.keywords_path, "r+") as filename:
                content_set = filename.read().splitlines()
                if keyword not in content_set:
                    filename.write("\n" + keyword.lower())

    def remove_keywords(self, keyword):
        # self.keywords.remove(keyword)
        if self.keywords_path != '':
            with open(self.keywords_path, "r") as filename:
                content_set = filename.read().splitlines()
                index = content_set.index(keyword.lower())

                content_set.remove(content_set[index])

            with open(self.keywords_path, "w") as filename:
                filename.write("\n".join(content_set))

    def create_set(self, set_name, keywords_list):
        # self.sets[set_name.lower()] = keywords_list

        if self.keywords_set_path != '':
            with open(self.keywords_set_path, "r") as readfile:
                read = readfile.read()
                if read != '':
                    self.sets = json.loads(read)
            self.sets[set_name.lower()] = keywords_list
            with open(self.keywords_set_path, "w") as writefile:
                json.dump(self.sets, writefile)

    def remove_set(self, set_name):
        # del self.sets[set_name.lower()]

        if self.keywords_set_path != '':
            with open(self.keywords_set_path, "r") as readfile:
                self.sets = json.loads(readfile.read())

            del self.sets[set_name.lower()]

            with open(self.keywords_set_path, 'w') as writefile:
                json.dump(self.sets, writefile)

    def get_set_values(self, set_name):
        if self.keywords_set_path != '':
            with open(self.keywords_set_path, "r") as readfile:
                self.sets = json.loads(readfile.read())

            return self.sets[set_name.lower()]

    def get_keywords(self):
        if self.keywords_path != '':
            with open(self.keywords_path, "r") as filename:
                self.keywords = filename.read().splitlines()

            return self.keywords

    def get_set(self):
        if self.keywords_set_path != '':
            with open(self.keywords_set_path, "r") as filename:
                self.sets = json.loads(filename.read())

            return self.sets

    def remove_keyword_from_set(self, keyword, set_name):
        if self.keywords_set_path != '':
            with open(self.keywords_set_path, "r") as readfile:
                self.sets = json.loads(readfile.read())

            list_value = list(self.sets[set_name])
            list_value.remove(keyword)
            self.sets[set_name] = list_value

            with open(self.keywords_set_path, "w") as writefile:
                json.dump(self.sets, writefile)


# code to test if the keywords class is working
if __name__ == '__main__':
    key = Keywords()

    while True:
        userInput = input("Type 1 for adding a keyword\n"
                          "Type 2 for removing a keyword\n"
                          "Type 3 to add a set\n"
                          "Type 4 to remove a set\n"
                          "Type 5 to view keywords\n"
                          "Type 6 to view sets\n"
                          "Type 7 to view values of a set\n"
                          "Type 8 to remove a keyword from a set\n"
                          "Type 0 to quit\n"
                          "Enter input: ")

        if userInput == '1':
            addWord = input("Type the keyword to add: ")
            key.add_keywords(addWord)
        elif userInput == '2':
            key.get_keywords()
            removeWord = input("Type keyword to remove: ")
            key.remove_keywords(removeWord)
        elif userInput == '3':
            setKey = input("Enter set name: ")
            setValues = input("Enter set values seperated by ',': ")
            key.create_set(setKey, setValues)
        elif userInput == '4':
            key.get_set()
            removeSet = input("Enter set name to remove: ")
            key.remove_set(removeSet)
        elif userInput == '5':
            print(key.get_keywords())
        elif userInput == '6':
            print(key.get_set())
        elif userInput == '7':
            st = input("enter set to get values: ")
            print(key.get_set_values(st))
        elif userInput == '8':
            st = input("enter set to remove keyword from: ")
            kw = input("enter keyword to remove: ")
            key.remove_keyword_from_set(kw, st)
        else:
            break
