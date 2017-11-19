import MySQLdb


def connection():
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           password="Whackamole12!",
                           df="flaskdb")
    c = conn.cursor()
    return c, conn
