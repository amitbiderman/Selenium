import sqlite3
import os


class Sql(object):
    def __init__(self, db_file_name):
        self.db_file_name = db_file_name

    def file_check(self):
        if os.path.exists(self.db_file_name):
            return True
        else:
            f = open(self.db_file_name, "x")
            f.close()
            print('Data base file created!')

    def create_table(self):
        with sqlite3.connect(self.db_file_name) as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS Items (
            id INT,
            name TEXT,
            price INT,
            description TEXT,
            date TEXT,
            city TEXT,
            url TEXT,
            PRIMARY KEY(id));""")
            conn.commit()
        return conn

    def insert(self, id, name, price, description, date, city, url):
        with sqlite3.connect("{}".format(self.db_file_name)) as conn:
            conn.execute(""
                         "INSERT OR REPLACE INTO Items ("
                         "id, name, price,  description, date, city, url)"
                         "VALUES (?, ?, ?, ?, ?, ?, ?);",
                         (id, name, price, description, date, city, url))
            conn.commit()

    def new_item(self, name_to_find):
        with sqlite3.connect(self.db_file_name) as conn:
            conn.row_factory = lambda mycursor, row: row[0]
            mycursor = conn.cursor()
            name_data = mycursor.execute("SELECT name FROM Items").fetchall()
        return name_to_find in name_data
