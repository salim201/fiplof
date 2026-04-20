import os
import sys
import os
import os.path
import psycopg2
import csv

class Importcsv:
    def __init__(self, connection):
        self.connection = connection

    def read(self):
        file = open("persphysToImport.csv")
        csvreader = csv.reader(file,',')
        header = next(csvreader)
        print(header)
        rows = []
        for row in csvreader:
            rows.append(row)
        print(rows)
        file.close()