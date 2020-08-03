import os
import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from .mykeywords import Search
from .database import Sql
from .Email import Email

"""
Program features:
* Allowing easy insert of search keywords and limiting products number from a different file!
* Going through as many search pages as needed
* Inserting all data to SQLite (creating file automatically) !
* Scrolling down page as search go to allow see products in real time
* Inserting only unique items to DB.
* Counting total search time and products found
* The user will delete items from the SQL db that are not relevant and will have access to URL's of the once who are.
# Sending daily report e-mail with changed prices and new items found:
# 1. Email details are in Email file
# 2. Must check "allow less secure apps: OFF" on receiver email first
* Option: to take keywords from mykeywords.text !
"""


# TODO
#  change mykeywords to take search info from text file or menu
#  the program will run every day for the same / different amount of items inserted (will not add items that are
#  already in the DB)

class Yad2(object):
    def __init__(self):
        self.keywords = Search("keys.txt")
        self.keywords.keys_file()
        self.driver = webdriver.Chrome("C:\\Program Files (x86)\\chromedriver.exe")
        self.y_scroll = 500
        self.vars = {}
        self.id = 1
        self.product_url = ''
        self.page_num = 2
        self.num_path_tracker = 0
        self.num_products = 0
        self.list_of_names = []
        self.is_first_search = False
        self.last_viewed_item = ''
        self.text = ''
        self.price_change = ''

    def search(self):
        self.driver.get("https://www.yad2.co.il/products/all")
        self.driver.maximize_window()
        time.sleep(3)
        self.driver.execute_script("window.scrollTo(0, {})".format(self.y_scroll))
        WebDriverWait(self.driver, 30000).until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".heading")))
        self.driver.find_element(By.CSS_SELECTOR, ".search_column:nth-child(2) > .search_select .text_input").click()
        self.driver.find_element(By.CSS_SELECTOR, ".search_column:nth-child(2) > .search_select .text_input").send_keys(
            self.keywords.search_category)
        self.driver.find_element(By.CSS_SELECTOR, "span > strong").click()
        self.driver.find_element(By.NAME, "info").send_keys(self.keywords.search_keyword)
        self.driver.find_element(By.CSS_SELECTOR, ".range_inputs > .y2_text:nth-child(1) .text_input").send_keys(
            self.keywords.lowest_price)
        self.driver.find_element(By.CSS_SELECTOR, ".y2_text:nth-child(2) .text_input").send_keys(self.keywords.highest_price)
        self.driver.find_element(By.CSS_SELECTOR, ".filter_btn").click()
        self.driver.find_element(By.CSS_SELECTOR, ".filter_btn").click()
        WebDriverWait(self.driver, 50000).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "#image_0 > .feedImage")))
        time.sleep(2)

    def collecting_data(self):
        while self.num_path_tracker != self.keywords.num_of_products:
            try:
                # scrolling down
                self.driver.execute_script("window.scrollTo(0, {})".format(self.y_scroll))
                # Waiting for element to be visible after scrolling down
                WebDriverWait(self.driver, 10).until(
                    expected_conditions.visibility_of_element_located((By.CSS_SELECTOR,
                                                                       "#feed_item_{} .container".format(
                                                                           self.num_path_tracker))))
                self.driver.find_element(By.CSS_SELECTOR,
                                         "#feed_item_{} .container".format(self.num_path_tracker)).click()
                time.sleep(2)
                # product name
                self.vars["name"] = self.driver.find_element(By.CSS_SELECTOR, "#accordion_wide_{} .title".format(
                    self.num_path_tracker)).text
                # avoiding duplicates !
                if not sql.new_item(self.vars["name"]):
                    # product description
                    self.vars["description"] = self.driver.find_element(By.CSS_SELECTOR, ".details_text").text
                    # product price
                    self.vars["price"] = self.driver.find_element(By.CSS_SELECTOR, ".classified_price > .price").text
                    # seller's city
                    self.vars["city"] = self.driver.find_element(By.ID, 'important_item_city_{}'.format(
                        self.num_path_tracker)).text
                    # product date
                    self.vars["date"] = self.driver.find_element(By.ID, 'important_item_updated_at_{}'.format(
                        self.num_path_tracker)).text
                    # product URL
                    self.driver.find_element(By.CSS_SELECTOR, '.new_tab > span:nth-child(2)').click()
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    self.product_url = self.driver.current_url
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    # closing item sub-window
                    self.driver.find_element(By.CSS_SELECTOR, ".y2i_close").click()
                    # scrolling down
                    self.y_scroll += 200
                    self.num_path_tracker += 1
                    self.num_products += 1
                    # printing items found
                    print("\r", "Found: ", self.num_products, " Items", end='', sep='', flush=True)
                    yad2.inserting_data()
                else:
                    self.driver.find_element(By.CSS_SELECTOR, ".y2i_close").click()
                    self.num_path_tracker += 1
                    self.y_scroll += 200
                    yad2.collecting_data()
            except NoSuchElementException:
                yad2.pages_check()
        return self.num_products

    def inserting_data(self):
        Sql.insert(self, self.id, self.vars["name"], self.vars["price"], self.vars["description"],
                   self.vars["date"], self.vars["city"], self.product_url)
        self.id += 1

    def pages_check(self):
        # If wanted number of products reached - pass this function
        if self.num_products != self.keywords.num_of_products:
            try:
                self.driver.find_element(By.LINK_TEXT, "{}".format(self.page_num)).click()
                self.page_num += 1
                self.num_path_tracker = 0
                time.sleep(5)
                yad2.collecting_data()
            except NoSuchElementException:
                exit()
        else:
            pass

    @staticmethod
    def time_took():
        total_time = float(abs(start - end))
        if total_time > 60:
            total_time = total_time / 60
            print("\nTime took:", "%.2f" % total_time, "Minutes")
        else:
            print("\nTime took:", "%.2f" % total_time, "Seconds")

    # Deleting file content, or creating it.
    def daily_report_file_check(self):
        if os.path.exists(self.keywords.status_file_name):
            file = open(self.keywords.status_file_name, "r+")
            file.truncate(0)
            file.close()
        else:
            f = open(self.keywords.status_file_name, 'w+')
            f.close()

    # Inserting content to daily report file
    def daily_report(self, x):
        with open(self.keywords.status_file_name, 'a') as f:
            f.write(x)

    # Checking prices updates of already saved items in DB
    def price_check(self):
        print("Checking prices of Yesterday's items...")
        try:
            with sqlite3.connect("{}".format(self.keywords.db_file_name)) as conn:
                conn.row_factory = lambda mycursor, row: row[0]
                mycursor = conn.cursor()
                url_data = mycursor.execute('SELECT url FROM Items').fetchall()
                price_data = mycursor.execute("SELECT price FROM Items").fetchall()
                name_data = mycursor.execute("SELECT name FROM Items").fetchall()
                num = 0
            for i in url_data:
                self.driver.get(url_data[num])
                self.driver.maximize_window()
                try:
                    WebDriverWait(self.driver, 3).until(
                        expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".price")))
                except TimeoutException:
                    self.driver.refresh()
                    WebDriverWait(self.driver, 3).until(
                        expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".price")))
                new_price = self.driver.find_element(By.CSS_SELECTOR, ".price").text
                if new_price != price_data[num]:
                    self.price_change = ("The price of the product: {} , has changed. Was:{}, Now:{}"
                                    .format(name_data[num], price_data[num], new_price[num]))
                    yad2.daily_report(self.price_change)
                num += 1
            print("All prices are up to date!")
        # If a DB file created before but with no items(script stopped)
        except sqlite3.OperationalError:
            print("No items in Data base, continuing.")
            pass

    # need to check again in a loop after an hour if up until self.last_viewed_item (that would be the last in the
    # second check) we found a new item
    def keep_checking(self):
        pass

    def teardown(self):
        if num_products != 0:
            self.text = ("Number of today's new products found: {}".format(num_products))
            yad2.daily_report(self.text)
        self.driver.close()

    def run(self):
        pass


def main():
    start = time.time()
    yad2 = Yad2()
    sql = Sql(yad2.keywords.db_file_name)
    # Checking before new items are added if file exists and if it does - checks price changes
    yad2.daily_report_file_check()
    if sql.file_check():
        yad2.price_check()
    yad2.search()
    sql.create_table()
    print("Searching...")
    num_products = yad2.collecting_data()
    end = time.time()
    if num_products == 0:
        print("No new items found!")
    yad2.time_took()
    yad2.teardown()
    if os.stat(yad2.keywords.status_file_name).st_size != 0:
        email = Email(yad2.keywords.status_file_name, yad2.keywords.gmail_sender, yad2.keywords.gmail_receiver,
                      yad2.keywords.gmail_password)
        email.send()


if __name__ == '__main__':
    main()
