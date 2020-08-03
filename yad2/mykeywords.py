import json
import os


# TODO
#  need to write menu 2
#  menu 1 works but need to assign real variables and return them to all files


class Setting(object):
    def __init__(self, name, description, data_type: type = str, ending=""):
        self.name = name
        self.description = description
        self.data_type = data_type
        self.data = None
        self.ending = ending
        if self.ending != "":
            assert self.data_type is str

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_from_user(self):
        if self.ending == "":
            extra_info = ""
        else:
            extra_info = f" (With {self.ending} ending!)"

        while True:
            data = input(f"Please enter {self.description}{extra_info}: ")

            try:
                if not data.endswith(self.ending):
                    print(f"Please enter the correct file ending ({self.ending})!")
                    continue

                self.data = self.data_type(data)
                break
            except ValueError:
                print("Please enter correct values!")

        return self.data

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data


class Search(object):
    def __init__(self, keys_file_name):
        self.keys_file_name = keys_file_name
        self.settings = [
            Setting("search_category", "Search Category"),
            Setting("search_keyword", "Search Keyword"),
            Setting("num_of_products", "Number of Products", data_type=int),
            Setting("lowest_price", "Lowest Price", data_type=int),
            Setting("highest_price", "Highest Price", data_type=int),
            Setting("db_file_name", "Data Base File Name", ending=".sqlite"),
            Setting("status_file_name", "Email-Status File Name", ending=".txt"),
            Setting("gmail_sender", "Email of sender"),
            Setting("gmail_receiver", "Email of receiver"),
        ]
        self.password_setting = Setting("gmail_password", "Email Sender Password (will be saved in a different file)")
        self.data_dict = {}

    def keys_file(self):
        # Checking "keys" file status
        # If file exists and has no content
        if os.path.exists(self.keys_file_name) and os.stat(self.keys_file_name).st_size == 0:
            print("File has no content, please fill key words!")
            self.change_all_settings()
        # If file doesn't exists
        elif not os.path.exists(self.keys_file_name):
            print("File Created! Please write new keywords!")
            f = open(self.keys_file_name, "x+")
            f.close()
            self.change_all_settings()
        # TODO: if file content is not the way it should be (someone re-wrote it) - need to call menu_2 again
        else:
            self.menu()

    def menu(self):
        while True:
            answer = input("Choose a number option:\n"
                           "1. To use keywords from file\n"
                           "2. To write new keywords\n"
                           "3. To read keywords from file\n"
                           "4. To exit program\n")
            if answer == "1":
                self.use_file()
                break
            elif answer == "2":
                self.write_menu()
            elif answer == "3":
                self.read_file()
            elif answer == "4":
                input("Good bye!\n"
                      "Press Enter to leave")
                break
            else:
                print('Please enter only 1, 2 3 or 4!\n')

    def use_file(self):
        with open(self.keys_file_name, 'r') as f:
            self.data_dict = json.load(f)

        for setting in self.settings:
            name = setting.get_name()
            if name in self.data_dict:
                setting.set_data(self.data_dict[name])

        with open('password.txt', 'r') as f:
            self.password_setting.set_data(json.load(f))

    # TODO: To be able to change only one parameter in the file
    def write_menu(self):
        while True:
            required_keyword = input("Enter a specific keyword or ALL (default: ALL): ").strip().lower()
            if required_keyword == "" or required_keyword == "all":
                self.change_all_settings()
                break

            self.use_file()
            if self.change_specific(required_keyword):
                self.write_file()
                break

    def change_specific(self, required_keyword):
        if self.password_setting.get_description().lower() == required_keyword:
            self.password_setting.get_from_user()
            return True

        for setting in self.settings:
            if setting.get_description().lower() == required_keyword:
                self.data_dict[setting.get_name()] = setting.get_from_user()
                return True

        print(f"Bad keyword name: {required_keyword}!")
        return False

    def change_all_settings(self):
        self.data_dict = {}
        for setting in self.settings:
            self.data_dict[setting.get_name()] = setting.get_from_user()

        self.password_setting.get_from_user()

        self.write_file()

        print("All keywords entered!")

    def write_file(self):
        with open(self.keys_file_name, 'w') as f:
            json.dump(self.data_dict, f)

        with open('password.txt', 'w+') as f:
            json.dump(self.password_setting.get_data(), f)

    def read_file(self):
        self.use_file()
        print("\n")
        for setting in self.settings:
            print(f"{setting.get_description()}: {setting.get_data()}")
        print("\n")


if __name__ == '__main__':
    search = Search("keys.txt")
    search.keys_file()
