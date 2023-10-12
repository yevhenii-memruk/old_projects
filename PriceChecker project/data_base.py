import mysql.connector
from database_info import user, password


class DataServer(object):
    def __init__(self):
        self.db = None

    def __enter__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user=user,
            passwd=password,
            database="testdatabase"
        )

        return self.db

    def __exit__(self, type, value, traceback):
        self.db.close()


if __name__ == "__main__":
    pass
