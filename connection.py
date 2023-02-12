import sqlite3
from tools import DATABASE


class ConnectDatabase:

    def __init__(self, querySQL, dataForQuery = []):
        
        self.con = sqlite3.connect(DATABASE)
        self.cur = self.con.cursor()
        self.res = self.cur.execute(querySQL, dataForQuery)

    def select_all(self):

        rows = self.res.fetchall() # Se capturan filas de datos
        columns = self.res.description # Se capturan nombres de columnas

        allRecords = []

        for row in rows:
            record = {}
            for position, column in enumerate(columns):
                record[column[0]] = row[position]
            allRecords.append(record)
        
        self.con.close()

        return allRecords

    def insert(self):
        self.con.commit()
        self.con.close()

    def delete_by(self):
        self.con.commit()
        self.con.close()