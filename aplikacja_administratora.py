#!/usr/bin/python

import raport_o_domokrazcach
import wyslij_stale
import wyslij
import wyszukiwanie_w_bazie
import usun_tabele
import stworz_baze
import dodaj_klienta

if __name__ == "__main__":
    
    program = True
    while program:
        print("Witaj w aplikacji klienckiej!")
        print("Menu:")
        print("Wciśnij 1, aby wysłać zapisane dane do serwera")
        print("Wciśnij 2, aby wygenerować raport o statystykach domokrążców")
        print("Wciśnij 3, aby wyszukać dane o wybranej osobie")
        print("Wciśnij 4, aby usunąć wszystkie tabele.")
        print("Wciśnij 5, aby wysłać testowe dane do bazy.")
        print("Wciśnij 6, aby stworzyć szkielet bazy danych")
        print("Wciśnij 7, aby dodać klienta")
        print("Wciśnij 8, aby zakończyć program")
        
        inp = input()

        if inp == '1':
            wyslij.wykonaj_kod()
            # try:
                # wyslij.wykonaj_kod()
            # except:
                # print("nie ma takiego adresu w bazie!! Poprawne dane zostały dodane.")
        elif inp == '2':
            raport_o_domokrazcach.wykonaj_kod()
        elif inp == '3':
            wyszukiwanie_w_bazie.wykonaj_kod()
        elif inp == '4':
            usun_tabele.wykonaj_kod()
        elif inp == '5':
            wyslij_testowe.wykonaj_kod()
        elif inp == '6':
            stworz_baze.wykonajkod()
        elif inp == '7':
            dodaj_klienta.wykonaj_kod()
        elif inp == '8':
            program = False
            
    print("Dziękujemy za skorzystanie z naszego programu")


        