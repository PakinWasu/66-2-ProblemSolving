import sqlite3
sqlfile = 'makroPB.db'
def get_node():
    try:
        sqliteConnection = sqlite3.connect(sqlfile)
        cursor = sqliteConnection.cursor()
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
            return(IDshelf)

def get_distanc():
    try:
        sqliteConnection = sqlite3.connect(sqlfile)
        cursor = sqliteConnection.cursor()
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
            return(edge)
    

def get_productname():
    try:
        sqliteConnection = sqlite3.connect(sqlfile)
        cursor = sqliteConnection.cursor()
        sqlite_select_query = """SELECT Product.Name FROM Product;"""
        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()
        proname = []
        for i in record:
            for k in i: 
                proname.append(k)
    except sqlite3.Error as error:
        print("Failed to read single row from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            return(proname)    
def get_idshelf_by_productname(pronames):
    try:
        sqliteConnection = sqlite3.connect(sqlfile)
        cursor = sqliteConnection.cursor()
        # สร้างสตริงสำหรับใช้ใน SQLite IN clause ด้วยจำนวนตัวแปรที่ถูกกำหนดโดยใช้ ? ในสตริง
        placeholders = ",".join("?" * len(pronames))
        sqlite_select_query = f"""SELECT Product.IDshelf FROM Product WHERE Product.Name IN ({placeholders});"""
        cursor.execute(sqlite_select_query, pronames)
        records = cursor.fetchall()
        idshelfs = []
        for record in records:
            idshelfs.append(record[0])
    except sqlite3.Error as error:
        print("Failed to read rows from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            return idshelfs
def get_pos_node():
    try:
        sqliteConnection = sqlite3.connect(sqlfile)
        cursor = sqliteConnection.cursor()
        sqlite_select_query = """SELECT Posmap.IDshelf,Posmap.x,Posmap.y FROM Posmap"""
        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()
        pos = {}
        for i in record:
            pos[i[0]] = i[1:]
    except sqlite3.Error as error:
        print("Failed to read single row from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
    return(pos)

def get_productname_by_idshelf(idshelf):
    try:
        sqliteConnection = sqlite3.connect(sqlfile)
        cursor = sqliteConnection.cursor()
       
        sqlite_select_query = f"""SELECT Product.Name FROM Product WHERE Product.IDshelf = ?;"""
        data = (idshelf)
        cursor.execute(sqlite_select_query,[data])
        records = cursor.fetchall()
        text = ""
        for item in records:
            if item == records[len(records)-1]:
                text += item[0]   
                break 

            text += item[0] + "\n"

        # print(text)
    except sqlite3.Error as error:
        print("Failed to read rows from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return(text)

#print(get_productname_by_idshelf('FV11'))
# pos = get_pos_node()
# print(pos)