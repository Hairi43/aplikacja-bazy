import zapisz


if __name__ == "__main__":


    # przykładowe dane do zapisu
    #
    #   ulica    nr_budynku   nr_mieszkania    kod_pocztowy   miasto
    #  Kwiatowa	    74	          4	             85-001	      Łódź
    #
    
    
    program = True
    while program:
        print("Witaj w aplikacji klienckiej!")
        print("Menu:")
        print("Wciśnij 1, aby zapisać odczyty liczników")
        print("Wciśnij 2, aby zakończyć program")

        inp = input()

        if inp == '1':
            zapisz.wykonaj_kod()
        elif inp == '2':
            program = False

    print("Dziękujemy za skorzystanie z naszego programu")


        