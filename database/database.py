import mysql.connector

def conectar_banco():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="9090",
        database="kamban"
    )

    return conn
    

