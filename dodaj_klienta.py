#!/usr/bin/python

import simplejson
import psycopg
import csv
import os
import datetime

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
    

    koniec = True
    czyID = False
            
    while koniec:

        print("Wpisz imię")
        imie = input()

        print("Wpisz nazwisko")
        nazwisko = input()

        print("Wpisz pesel")
        pesel = input()

        print("Wpisz ulicę")
        ulica = input()
    
        print("Wpisz nr budynku")
        nr_budynku = input()
    
        print("Wpisz nr mieszkania")
        nr_mieszkania = input()
    
        print("Wpisz kod pocztowy")
        kod_pocztowy = input()
    
        print("Wpisz miejscowość")
        miejscowosc = input()
             

        # jeżeli nie ma klienta lub adresu poczty w bazie to go dodaje
        c.execute(f"""SELECT 1 FROM klienci WHERE imie = '{imie}' and nazwisko = '{nazwisko}' and pesel = '{pesel}';""")
        ilosc_rekordow_klient = c.fetchall()

        c.execute(f"""SELECT 1 FROM adres_pocztowy WHERE kod_pocztowy = '{kod_pocztowy}' and miejscowosc = '{miejscowosc}';""")
        ilosc_rekordow_adresy_pocztowe = c.fetchall()

        if ilosc_rekordow_klient == []:
            c.execute(f"""INSERT INTO klienci (imie, nazwisko, pesel) VALUES ('{imie}', '{nazwisko}', '{pesel}');""")

        if ilosc_rekordow_adresy_pocztowe == []:
            c.execute(f"""INSERT INTO adres_pocztowy (kod_pocztowy, miejscowosc) VALUES ('{kod_pocztowy}', '{miejscowosc}');""")


        # dodanie adresu do klienta
        c.execute(f"""SELECT id_klienta FROM klienci WHERE imie = '{imie}' and nazwisko = '{nazwisko}' and pesel = '{pesel}';""")
        id_klienta = c.fetchall()


        c.execute(f"""SELECT id_adres_pocztowy FROM adres_pocztowy WHERE kod_pocztowy = '{kod_pocztowy}' and miejscowosc = '{miejscowosc}';""")
        id_adres_pocztowy = c.fetchall()


        # dodanie adresu klienta do bazy
        if nr_mieszkania == '':
            c.execute("""
                INSERT INTO adres_klienta (ulica, nr_budynku, nr_mieszkania, id_adres_pocztowy, id_klienta) VALUES (%s, %s, %s, %s, %s)
                """, (ulica, int(nr_budynku), None, int(id_adres_pocztowy[0][0]), int(id_klienta[0][0])))
        else:
            c.execute("""
                INSERT INTO adres_klienta (ulica, nr_budynku, nr_mieszkania, id_adres_pocztowy, id_klienta) VALUES (%s, %s, %s, %s, %s)
                """, (ulica, int(nr_budynku), int(nr_mieszkania), int(id_adres_pocztowy[0][0]), int(id_klienta[0][0])))


        aktualna_data = datetime.datetime.now().strftime("%Y-%m-%d")
        print(aktualna_data)
        # c.execute('INSERT INTO liczniki (data_ostatniej_instalacji) VALUES (?)', aktualna_data)
        c.execute(f"""INSERT INTO liczniki (data_ostatniej_instalacji) VALUES ('{aktualna_data}')""")
        
            
        ####
        ####   DOKOŃCZYĆ
        ####
        ####   Dodać sprawdzanie adresu klienta czy jest w bazie, bo jak jest to ma odrzucić
        ####
        #### może trzeba będzie dodać osobne przerzucanie danych do historii licznika
            # dodać datę instalacji do liczników

        print("Dodano klienta z adresem!")
        
        print("zakończyć wpisywanie? wpisz t jeśli tak, jeśli chcesz dalej wpisywać kliknij enter")
        sprawdz = input()
        
        if sprawdz == 't':
            koniec = False
            
    connection.commit()
    connection.close()


if __name__ == "__main__":
    wykonaj_kod()
