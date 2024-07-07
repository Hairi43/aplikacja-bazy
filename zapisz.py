#!/usr/bin/python

import sqlite3
import csv
import datetime

# puste_id_adresu = -1;

def wykonaj_kod():

    conn = sqlite3.connect('dane')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS zebrane_dane (
            id_wpisu serial primary key,
            zuzycie float,
            data_odczytu date,
            nr_identyfikacji int,
            ulica text not null,
            nr_budynku int,
            nr_mieszkania int,
            kod_pocztowy text not null,
            miejscowosc text not null
        )""")
    conn.commit()
    
    def Zapisz_dane_w_bazie(zuzycie, aktualna_data, nr_identyfikacji, ulica, nr_budynku, nr_mieszkania, kod_pocztowy, miejscowosc):
        if nr_mieszkania == None:
            dane = [float(zuzycie), aktualna_data, int(nr_identyfikacji), ulica, int(nr_budynku), None, kod_pocztowy, miejscowosc]
            c.execute('INSERT INTO zebrane_dane (zuzycie, data_odczytu, nr_identyfikacji, ulica, nr_budynku, nr_mieszkania, kod_pocztowy, miejscowosc) VALUES (?,?,?,?,?,?,?,?)', dane)
            conn.commit()
        else:
            dane = [float(zuzycie), aktualna_data, int(nr_identyfikacji), ulica, int(nr_budynku), int(nr_mieszkania), kod_pocztowy, miejscowosc]
            c.execute('INSERT INTO zebrane_dane (zuzycie, data_odczytu, nr_identyfikacji, ulica, nr_budynku, nr_mieszkania, kod_pocztowy, miejscowosc) VALUES (?,?,?,?,?,?,?,?)', dane)
            conn.commit()
    
    def Aktualizuj_w_bazie(zuzycie, aktualna_data, nr_identyfikacji, ulica, nr_budynku, nr_mieszkania, kod_pocztowy, miejscowosc):
        if nr_mieszkania == None:
            dane = [float(zuzycie), aktualna_data, int(nr_identyfikacji), ulica, int(nr_budynku), None, kod_pocztowy, miejscowosc]
            c.execute('UPDATE zebrane_dane SET zuzycie = ?, data_odczytu = ?, nr_identyfikacji = ? WHERE ulica = ? and nr_budynku = ? and nr_mieszkania = ? and kod_pocztowy = ? and miejscowosc = ?', dane) 
            conn.commit()
        else:
            dane = [float(zuzycie), aktualna_data, int(nr_identyfikacji), ulica, int(nr_budynku), int(nr_mieszkania), kod_pocztowy, miejscowosc]
            c.execute('UPDATE zebrane_dane SET zuzycie = ?, data_odczytu = ?, nr_identyfikacji = ? WHERE ulica = ? and nr_budynku = ? and nr_mieszkania = ? and kod_pocztowy = ? and miejscowosc = ?', dane) 
            conn.commit()

    # pokazuje aktualnie zapisane rekordy w bazie danych
    print("zapisane rekordy w bazie")
    for rekord in c.execute("""SELECT * FROM zebrane_dane"""):
        print(rekord)

    # rozpoczyna wpisywanie danych do bazy
    koniec = True
    czyID = False
    print("Wpisz nr identyfikacji")
    nr_identyfikacji = input()
            
    while koniec:
    
        print("Wpisz ulicę")
        ulica = input()
    
        print("Wpisz nr budynku")
        nr_budynku = input()
    
        print("Wpisz nr mieszkania")
        nr_mieszkania = input()
        if nr_mieszkania == '':
            nr_mieszkania = None
    
        print("Wpisz kod pocztowy")
        kod_pocztowy = input()
    
        print("Wpisz miejscowość")
        miejscowosc = input()
    
        print("Wpisz zuzycie")
        zuzycie = input()
             
        # sprawdzenie czy dane z tego dnia są już w bazie oraz dalsze zapisanie/zaktualizaowanie ich
        for rekord in c.execute("""SELECT * FROM zebrane_dane"""):
            if str(rekord[4]) == str(ulica) and str(rekord[5]) == str(nr_budynku) and str(rekord[6]) == str(nr_mieszkania) and str(rekord[7]) == str(kod_pocztowy) and str(rekord[8]) == str(miejscowosc):
                czyID = True
        aktualna_data = datetime.datetime.now().strftime("%Y-%m-%d")
        if czyID == True:
            czyID = False
            print("podano adres, który już jest w bazie danych, czy chcesz zaktualizować wpisane zuzycie?")
            print("wpisz t lub n")
            zaktualizuj = input()
            if zaktualizuj == "t":
                Aktualizuj_w_bazie(zuzycie, aktualna_data, nr_identyfikacji, ulica, nr_budynku, nr_mieszkania, kod_pocztowy, miejscowosc)
        else:
            Zapisz_dane_w_bazie(zuzycie, aktualna_data, nr_identyfikacji, ulica, nr_budynku, nr_mieszkania, kod_pocztowy, miejscowosc)
        print("zakończyć wpisywanie? wpisz t jeśli tak, jeśli chcesz dalej wpisywać kliknij enter")
        sprawdz = input()
        
        if sprawdz == 't':
            koniec = False


    # zapisywanie/nadpisywanie do pliku csv
    dane = []
    for rekord in c.execute("SELECT * FROM zebrane_dane"):
        tmp =  rekord[1], rekord[2], rekord[3], rekord[4], rekord[5], rekord[6], rekord[7], rekord[8]
        dane.append(tmp)
        
    with open('zebrane_dane.csv', 'w') as plik:
        w = csv.writer(plik)
        w.writerow(['zuzycie', 'data_odczytu', 'nr_identyfikacji', 'ulica', "nr_budynku", "nr_mieszkania", "kod_pocztowy", "miejscowosc"])
        w.writerows(dane)
        
        for rekord in c.execute("SELECT * FROM zebrane_dane"):
            print(rekord)
    
    conn.close()



if __name__ == "__main__":
    wykonaj_kod()
    