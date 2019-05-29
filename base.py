import sqlite3

class Base:
    """this is context manager to create connection to database (if base doesn't exists it
    will be created"""
    def __init__(self, dbname):
        self.name = dbname

    def __enter__(self):
        self.con = sqlite3.connect(self.name)
        return self.con

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.con.commit()
            print('commit successful')
        except sqlite3.Error as err:
            print(err)
        self.con.close()