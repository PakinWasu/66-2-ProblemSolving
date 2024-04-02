import sqlite3
sqlfile = 'makroPB.db'
def get_node():
    try:
        sqliteConnection = sqlite3.connect(sqlfile)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_select_query = """SELECT IDshelf 
                                FROM Shelf;"""
        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()
        IDshelf = []
        for i in record:
            for n in i :
                IDshelf.append(n)
    except sqlite3.Error as error:
        print("Failed to read single row from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
            return(IDshelf)

def get_distanc():
    try:
        sqliteConnection = sqlite3.connect(sqlfile)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_select_query = """SELECT nodesrc,nodedest,weigh FROM Distanc;"""
        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()
        edge = []
        for i in record:
            edge.append(i)
    except sqlite3.Error as error:
        print("Failed to read single row from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
            return(edge)
    
    
            

    