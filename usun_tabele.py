#!/usr/bin/python

import simplejson
import psycopg
import csv
import os

def wykonaj_kod():

    with open("db_con_file.json") as db_con_file:
        creds = simplejson.loads(db_con_file.read())
    
    connection = psycopg.connect(
        host=creds['host_name'],
        user=creds['user_name'],
        dbname=creds['db_name'],
        password=creds['password'],
        port=creds['port_number'])

    c = connection.cursor()

    c.execute("""DROP TABLE IF EXISTS klienci, adres_klienta, liczniki, adres_pocztowy, domokrazcy, historia_licznika, odczyty_licznika CASCADE;""")
    
    connection.commit()
    connection.close()


if __name__ == "__main__":
    wykonaj_kod()
