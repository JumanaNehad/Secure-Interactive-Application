import mysql.connector

def connectdb():
    # Connect to the database
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='sia')

    # Create a cursor object
    cursor = conn.cursor()
    ##cursor.execute("SELECT * FROM `white`")
    
    
    ##print(cursor.fetchall())
    return conn, cursor
