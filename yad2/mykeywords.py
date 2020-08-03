import json
import os


# TODO
#  need to write menu 2
#  menu 1 works but need to assign real variables and return them to all files


class Search(object):
    def __init__(self, keys_file_name):
        self.keys_file_name = keys_file_name
        self.words = ''
        self.categories = []
        self.search_category = None
        self.search_keyword = None
        self.num_of_products = None
        self.lowest_price = None
        self.highest_price = None
        self.db_file_name = None
        self.status_file_name = None
        self.gmail_sender = None
        self.gmail_receiver = None
        self.gmail_password = None

    def keys_file(self):
        # Checking "keys" file status
        # If file exists and has no content
        if os.path.exists(self.keys_file_name) and os.stat(self.keys_file_name).st_size == 0:
            print("File has no content, please fill key words!")
            self.menu_2()
        # If file doesn't exists
        elif not os.path.exists(self.keys_file_name):
            print("File Created! Please write new keywords!")
            f = open(self.keys_file_name, "x+")
            f.close()
            self.menu_2()
        # TODO: if file content is not the way it should be (someone re-wrote it) - need to call menu_2 again
        else:
            self.menu()

    def menu(self):
        answer = input("Choose a number option:\n"
                       "1. To use keywords from file\n"
                       "2. To write new keywords\n"
                       "3. To read keywords from file\n"
                       "4. To exit program\n")
        if answer == "1":
            self.menu_1()
        elif answer == "2":
            self.menu_2()
        elif answer == "3":
            self.menu_3()
        elif answer == "4":
            input("Good bye!\n"
                  "Press Enter to leave")
            return 1
        else:
            print('Please enter only 1, 2 or 3!!\n')
            self.menu()

    def menu_1(self):
        with open(self.keys_file_name, 'r') as f:
            d = json.load(f)

        for key in d:
            value = d[key]
            setattr(self, key, value)

        with open('password.txt', 'r') as f:
            self.gmail_password = json.load(f)

    def menu_2(self):
        try:
            data = {"search_category": input("Please enter Search Category"),
                    "search_keyword": input("Please enter Search Keyword"),
                    "num_of_products": int(input("Please enter Number of Products")),
                    "lowest_price": int(input("Please enter Lowest Price")),
                    "highest_price": int(input("Please enter Highest Price")),
                    "db_file_name": input("Please enter Data Base File Name (With sqlite ending!!)"),
                    "status_file_name": input("Please enter Email-Status File Name"),
                    "gmail_sender": input("Please enter Email of sender"),
                    "gmail_receiver": input("Please enter Email of receiver"),
                    "gmail_password": input("Please enter password of sender (Will be saved in a different file)")}
            while True:
                if not data["data_base_file_name"].endswith('.sqlite'):
                    data["data_base_file_name"] = input("Please enter Data Base File Name (With .sqlite ending!)")
                else:
                    break
            while True:
                if not data["status_file_name"].endswith('.txt'):
                    data["status_file_name"] = input("Please enter Email-Status File Name (With .txt ending!)")
                else:
                    break
            with open(self.keys_file_name, 'w') as f:
                json.dump(data, f)
            with open('password.txt', 'w+') as f:
                json.dump(self.gmail_password, f)
            print("All keywords entered!")

            self.menu()
        except ValueError:
            print("Please enter correct values!")
            self.menu_2()

    def menu_3(self):
        categories_show = ["Search Category", "Search Keyword", "Number of Products", "Lowest Price",
                           "Highest Price", "Data Base File Name", "Email-Status File Name"]
        num = 0
        print("\n")
        with open(self.keys_file_name, 'r') as f:
            self.words = json.load(f)
            for i in self.words.values():
                print(categories_show[num], ":", i)
                num += 1
        print("\n")
        self.menu()


# to make a file not exists yet

# [search_category, search_keyword, num_of_products, lowest_price, highest_price, db_file_name, status_file_name] = whip.values()
# asked if user want to tke keywords from file or not
# to make a show keywords from file option too !
# choice.lower == yes made:
# open file as f:
#  self.whip = eval(s)
# search_category, search_keyword ....  = whip.values()

""" IF NOT WORKING THEN SOMETHING FROM HERE : https://stackoverflow.com/questions/4803999/how-to-convert-a-file-into-a-dictionary"""
# if choice.lower == not - made:
#     data = {}
#     data["search_category"] = input  search_category
#     data["search_keyword"] = input  search_category
#     data["lowest_price"] = int(input  search_category)
#     data["highest_price"] = int(input  search_category)
#     data["data_base_file_name"] = data_base_file_name)
#     data["status_file_name] = data_base_file_name)
# NEED TO FIND DIFFERENT NAMES FOR FILES!!!

# class Search(object):
#
#     search_category = "ריהוט"
#     search_keyword = "מדף"
#     lowest_price = "200"
#     highest_price = "500"
#     db_file_name = "../shelf.sqlite"
#     status_file_name = "../status.txt"
#     num_of_products = 2
#     with open("../Email.txt", "r") as f:
#         email_content = f.read()
#     email_content = email_content.split('\n')
#     gmail_sender = email_content[0]
#     gmail_password = email_content[1]
#     if len(email_content) == 3:
#         gmail_reciever = email_content[2]
#     else:
#         gmail_reciever = gmail_sender

if __name__ == '__main__':
    search = Search("keys.txt")
    search.keys_file()
