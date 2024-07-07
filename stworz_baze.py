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
    
    # Najpierw tworzymy tabelę klienci
    c.execute("""
    CREATE TABLE IF NOT EXISTS klienci (
        id_klienta serial primary key,
        imie text,
        nazwisko text,
        pesel text not null
    )
    """)
    
    # Następnie tworzymy tabelę liczniki
    c.execute("""
    CREATE TABLE IF NOT EXISTS liczniki (
        id_licznika serial primary key,
        data_ostatniej_instalacji date not null
    )
    """)
    
    # Następnie tworzymy tabelę domokrazcy
    c.execute("""
    CREATE TABLE IF NOT EXISTS domokrazcy (
        id_domokrazcy serial primary key,
        imie text not null,
        nazwisko text not null,
        nr_identyfikacji int not null
    )
    """)


    c.execute("""
    CREATE TABLE IF NOT EXISTS adres_pocztowy (
        id_adres_pocztowy serial primary key,
        kod_pocztowy text not null,
        miejscowosc text not null
    )
    """)

    # Następnie tworzymy tabelę adresy
    c.execute("""
    CREATE TABLE IF NOT EXISTS adres_klienta (
        id_adres_klienta serial primary key,
        ulica text not null,
        nr_budynku int not null,
        nr_mieszkania int,
        id_adres_pocztowy int not null,
        id_klienta int not null,
        FOREIGN KEY (id_klienta) REFERENCES klienci(id_klienta),
        FOREIGN KEY (id_adres_pocztowy) REFERENCES adres_pocztowy(id_adres_pocztowy)
    )
    """)

    
    # Następnie tworzymy tabelę historia odczytów licznika
    c.execute("""
    CREATE TABLE IF NOT EXISTS odczyty_licznika (
        id_odczytu serial primary key,
        id_licznika int not null,
        data_odczytu date not null,
        zuzycie float not null,
        id_domokrazcy int not null,
        FOREIGN KEY (id_licznika) REFERENCES liczniki(id_licznika),
        FOREIGN KEY (id_domokrazcy) REFERENCES domokrazcy(id_domokrazcy)
    )
    """)
    
    # Następnie tworzymy tabelę historia adresów, w których licznik był umieszczony
    c.execute("""
    CREATE TABLE IF NOT EXISTS historia_licznika (
        id_miejsca serial primary key,
        id_licznika int not null,
        data_zalozenia date not null,
        data_usuniecia date,
        FOREIGN KEY (id_licznika) REFERENCES liczniki(id_licznika)
    )
    """)

    
    connection.commit()
    connection.close()
    

if __name__ == "__main__":
    wykonaj_kod()