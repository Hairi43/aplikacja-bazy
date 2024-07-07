import simplejson
import psycopg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def wykonaj_kod():

    with open("db_con_file.json") as db_con_file:
        creds = simplejson.loads(db_con_file.read())

    connection = psycopg.connect(
        host=creds['host_name'],
        user=creds['user_name'],
        dbname=creds['db_name'],
        password=creds['password'],
        port=creds['port_number'])
    
    def wyszukaj_dane_o_kliencie(imie, nazwisko, pesel):
        c = connection.cursor()
        c.execute(f"""SELECT klienci.imie, klienci.nazwisko, klienci.pesel, adres_klienta.ulica, adres_klienta.nr_budynku, adres_klienta.nr_mieszkania, 
                     adres_pocztowy.kod_pocztowy, adres_pocztowy.miejscowosc, odczyty_licznika.zuzycie, 
                     odczyty_licznika.data_odczytu, historia_licznika.data_zalozenia, historia_licznika.data_usuniecia 
                     FROM klienci
                     JOIN adres_klienta ON adres_klienta.id_klienta = klienci.id_klienta
                     JOIN adres_pocztowy ON adres_pocztowy.id_adres_pocztowy = adres_klienta.id_adres_pocztowy
                     JOIN liczniki ON adres_klienta.id_adres_klienta = liczniki.id_licznika
                     JOIN historia_licznika ON historia_licznika.id_licznika = liczniki.id_licznika
                     JOIN odczyty_licznika ON odczyty_licznika.id_licznika = liczniki.id_licznika
                     WHERE imie='{imie}' AND nazwisko='{nazwisko}' and pesel='{pesel}';""")
        dane = c.fetchall()
        # wypisanie danych przy pomocy pandas
        wypisz = pd.DataFrame(dane, columns=['imie', 'nazwisko', 'pesel', 'ulica', 'nr budynku', 'nr mieszkania', 'kod pocztowy', 'miejscowość', 'zużycie', 'data odczytu','data załóżenia licznika', 'data usunięcia licznika'])
        print(wypisz)
        return wypisz

    print("Wpisz imię szukanej osoby")
    imie = input()
    print("Wpisz nazwisko szukanej osoby")
    nazwisko = input()
    print("Wpisz pesel szukanej osoby")
    pesel = input()
    # wyszukaj_dane_o_kliencie('Paweł', 'Kowalczyk')
    wyszukaj_dane_o_kliencie(imie, nazwisko, pesel)
    connection.close()


if __name__ == "__main__":
    wykonaj_kod()