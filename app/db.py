import pymysql
import pymysql.cursors

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='flask_full_stack',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True, # now don't do commit manually after every query, it will be done automatically
    )

# * Note : if you are not adding the autocommit=True, then you have to do commit after every query manually, otherwise the changes will not be reflected in the database.