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
        pesel char(13) not null
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
        kod_pocztowy char(6) not null,
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

    

    # Wstawianie danych do tabeli osoby
    with open('csv/klienci.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(csv_reader)  # Pominięcie nagłówka
    
        for row in csv_reader:
            imie, nazwisko, pesel = row
    
            c.execute("""
                INSERT INTO klienci (imie, nazwisko, pesel) VALUES (%s, %s, %s)
                """, (imie, nazwisko, pesel))
    
    # Wstawianie danych do tabeli liczniki
    with open('csv/liczniki.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(csv_reader)  # Pominięcie nagłówka
    
        for row in csv_reader:
            data_ostatniej_instalacji = row
    
            c.execute("""
                INSERT INTO liczniki (data_ostatniej_instalacji)  VALUES (%s)
                """, (data_ostatniej_instalacji))
    
    # Wstawianie danych do tabeli domokrazcy
    # tu jest problem z syntaxem
    with open('csv/domokrazcy.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(csv_reader)  # Pominięcie nagłówka
        for row in csv_reader:
            imie, nazwisko, nr_identyfikacji = row
            c.execute("""
                INSERT INTO domokrazcy (imie, nazwisko, nr_identyfikacji) VALUES (%s, %s, %s)
                """, (imie, nazwisko, int(nr_identyfikacji)))

        # Wstawianie danych do tabeli adresy
    with open('csv/adres_pocztowy.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(csv_reader)  # Pominięcie nagłówka
    
        for row in csv_reader:
            kod_pocztowy, miejscowosc = row
    
            c.execute("""
                INSERT INTO adres_pocztowy (kod_pocztowy, miejscowosc) VALUES (%s, %s)
                """, (kod_pocztowy, miejscowosc))
            
    
    # Wstawianie danych do tabeli adresy
    with open('csv/adres_klienta.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(csv_reader)  # Pominięcie nagłówka
    
        for row in csv_reader:
            ulica, nr_budynku, nr_mieszkania, id_adres_pocztowy, id_klienta = row

            if nr_mieszkania == '':
                c.execute("""
                    INSERT INTO adres_klienta (ulica, nr_budynku, nr_mieszkania, id_adres_pocztowy, id_klienta) VALUES (%s, %s, %s, %s, %s)
                    """, (ulica, int(nr_budynku), None, int(id_adres_pocztowy), int(id_klienta)))
            else:
                c.execute("""
                    INSERT INTO adres_klienta (ulica, nr_budynku, nr_mieszkania, id_adres_pocztowy, id_klienta) VALUES (%s, %s, %s, %s, %s)
                    """, (ulica, int(nr_budynku), int(nr_mieszkania), int(id_adres_pocztowy), int(id_klienta)))
    
                      
    # Wstawianie danych do tabeli odczyty licznika
    with open('csv/odczyty_licznika.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(csv_reader)  # Pominięcie nagłówka
    
        for row in csv_reader:
            id_licznika, data_odczytu, zuzycie, id_domokrazcy = row
    
            c.execute("""
                INSERT INTO odczyty_licznika (id_licznika, data_odczytu, zuzycie, id_domokrazcy) VALUES (%s, %s, %s, %s)
                """, (int(id_licznika), data_odczytu, float(zuzycie), int(id_domokrazcy)))
    
    
    # Wstawianie danych do tabeli historia licznika
    with open('csv/historia_licznika.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(csv_reader)  # Pominięcie nagłówka
    
        for row in csv_reader:
            id_licznika, id_adres_klienta, data_zalozenia, data_usuniecia = row

            c.execute("""
                INSERT INTO historia_licznika (id_licznika, id_adres_klienta, data_zalozenia, data_usuniecia) VALUES (%s, %s, %s, %s)
                """, (int(id_licznika), int(id_adres_klienta), data_zalozenia, data_usuniecia))

    connection.commit()
    connection.close()
    

if __name__ == "__main__":
    wykonaj_kod()