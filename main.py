import urllib.request
import sqlite3
import sys
import logging
import os.path
from os import path


def main():
    conn = sqlite3.connect('transport.db')
    c = conn.cursor()
    c.row_factory= sqlite3.Row
    update_db('https://data.montpellier3m.fr/sites/default/files/ressources/TAM_MMM_TpsReel.csv', 'Montpellier.csv')
    create_schema(c)
    load_csv('Montpellier.csv', c)
    conn.commit()


def load_csv(path, cursor):
    """ This function load and read the csv file, and insert row in db file.

    cursor : It acts like a position indicator and will be mostly use to
    retrieve data.

    path : Source of the csv file.

    """
    with open(path, "r") as f:    
        f.readline()
        line = f.readline()
        while line:
            insert_csv_row(line, cursor)
            line = f.readline()
    # logging.info('load_csv: Charge la base de données')




def update_db(csv_url, outputfile):
    """This function, retrieve the csv from url and download this csv file

    """
    urllib.request.urlretrieve(csv_url, outputfile)
    # logging.info('update_db: Mise a jour de la base de données')



def insert_csv_row(csv_row, cursor):
    """ This function insert values in table 'infoarret'

    cursor : It acts like a position indicator and will be mostly use to
    retrieve data.

    csv_row : retrieve the lines on the csv file.

    """
    liste_row = csv_row.strip().split(";")
    new_row = [liste_row[3], liste_row[4], liste_row[5], liste_row[7], "Montpellier"]
    cursor.execute("""INSERT INTO infoarret VALUES (?,?,?,?,?) """,new_row)




# def list_ville(index):
#     list_ville = ['Montpellier','Rennes','Toulouse', 'Lyon']
#     return list_ville[index]



def create_schema(cursor):
    """ This function create table 'infoarret' if not exist

    this table contains 11 columns and determinate the type.

    cursor : It acts like a position indicator and will be mostly use to
    retrieve data.

    """
    # cursor.execute("""DROP TABLE IF EXISTS "infoarret" """)
    cursor.execute("""DROP TABLE IF EXISTS "infoarret" """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS "infoarret" (
    "Station"	TEXT,
    "Ligne"	TEXT,
    "Direction"	TEXT,
    "Horaire"	TEXT,
    "Ville" TEXT
    );""")
    
""" Use this function to show all the transport Stations available by entering '/stations' """
def stations():
    conn = sqlite3.connect('transport.db')
    c = conn.cursor()
    c.row_factory= sqlite3.Row
    c.execute("""SELECT Station FROM infoarret """)
    result = []
    for row in c.fetchall():
        result.append(dict(row))
    return result

""" Use this function to show all the transport lines available by entering 'line' """
def Ligne():
    conn = sqlite3.connect('transport.db')
    c = conn.cursor()
    c.row_factory= sqlite3.Row
    c.execute("""SELECT Ligne FROM infoarret """)
    result = []
    for row in c.fetchall():
        if dict(row) not in result or not result:
            result.append(dict(row))
    return result


""" Use this function to show all the next Bus/Tram coming to your stations by entering your station name"""
def next_transports(station):
    conn = sqlite3.connect('transport.db')
    c = conn.cursor()
    c.row_factory= sqlite3.Row
    c.execute("""SELECT Station,Direction,Ligne,Horaire FROM infoarret WHERE Station = ? """,
    (station.upper(),))
    result= []
    for row in c.fetchall():
        result.append(dict(row))
    return result
""" Use this function to show all the stations that the Tram will pass through by entering your the Line number """
def ligne_search(ligne):
    conn = sqlite3.connect('transport.db')
    c = conn.cursor()
    c.row_factory= sqlite3.Row
    c.execute("""SELECT Station FROM infoarreT WHERE Ligne = ? """,
    (ligne.upper(),))
    result = []
    for row in c.fetchall():
        if dict(row) not in result or not result:
            result.append(dict(row))
    return result           
""" Use this function to show the next Bus/Tram coming from 'A' to 'B' by entering the (Line number, Station Name, Direction Name) """
def next_line_station_direction(args1,args2,args3):
    conn = sqlite3.connect('transport.db')
    c = conn.cursor()
    c.row_factory= sqlite3.Row
    c.execute("""SELECT * FROM infoarret WHERE Ligne=? AND Station=? AND Direction=? ORDER BY Horaire""",(args1.upper(),args2.upper(),args3.upper(),))
    result =[]
    for i in c.fetchall():
        result.append(dict(i))
    return result



if __name__ == "__main__":
    sys.exit(main())



