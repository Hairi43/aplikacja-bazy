#!/usr/bin/python

import simplejson
import psycopg
import csv
import os
from datetime import datetime

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

    # try except nie wyrzuca błedu kiedy nie ma plików
    try:
        with open('zebrane_dane.csv', newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(csv_reader)  
        
            for row in csv_reader:
                zuzycie, data_odczytu, id_domokrazcy, ulica, nr_budynku, nr_mieszkania, kod_pocztowy, miejscowosc = row
        
                c.execute("""
                    SELECT ulica, nr_budynku, nr_mieszkania, kod_pocztowy, miejscowosc, id_licznika FROM adres_klienta
                    JOIN adres_pocztowy ON adres_klienta.id_adres_pocztowy = adres_pocztowy.id_adres_pocztowy
                    JOIN liczniki ON adres_klienta.id_adres_klienta = liczniki.id_licznika
                """)
                records = c.fetchall()
                
                id_licznika = -1
                for x in records:
                    if str(x[0]) == str(ulica) and str(x[1]) == str(nr_budynku) and str(x[2]) == str(nr_mieszkania) and str(x[3]) == str(kod_pocztowy) and str(x[4]) == str(miejscowosc):
                        id_licznika = x[5]
                if(id_licznika == -1):
                    print(f"nie ma takiego adresu w bazie!! -> {ulica, nr_budynku, nr_mieszkania, kod_pocztowy, miejscowosc}")
                    continue
                print(f"dodano odczyt licznika -> {ulica, nr_budynku, nr_mieszkania, kod_pocztowy, miejscowosc}")
                c.execute("""
                    INSERT INTO odczyty_licznika(id_licznika, data_odczytu, zuzycie, id_domokrazcy) VALUES (%b, %t, %b, %b)
                    """, (int(id_licznika), data_odczytu, float(zuzycie), int(id_domokrazcy)))
    
        connection.commit()
        connection.close()
    except:
        print("nie ma żadnych plików do wysłania")

    # usuwanie tymczasowej bazy i pliku csv
    # try except nie wyrzuca błedu kiedy nie ma plików
    try:
        file_path = os.path.join(os.getcwd(), "dane")
        os.remove(file_path)
    except:
        pass
    try:
        file_path = os.path.join(os.getcwd(), "zebrane_dane.csv")
        os.remove(file_path)
    except:
        pass

if __name__ == "__main__":
    wykonaj_kod()
