import os

# Setup funktion til at spørge brugeren om login og hvilken vagtplan der ønskes
def setup():
    list = []
    USER_INPUT = None
    # Tjekker om der allerede findes en config fil, hvis ja spørger om login oplysniger skal genbruges
    # hvis nej spørger brugeren om login og hvilken vagtplan der ønskes
    if os.path.exists('config.py'): 
        ask = input("Vil du bruge gemt brugernavn/adgangskode? (y/n) ")
        if ask == "n":
            user_input_brugernavn = input("Indtast brugernavn ")
            user_input_adgangskode = input("Indtast adgangskode ")
            vagtplan = input("Hvilken vagtplan vil du have? (aktuel/næste/) ")
        elif ask == 'y':
            import config
            user_input_brugernavn = config.user_brugernavn
            user_input_adgangskode = config.user_adgangskode
            vagtplan = input("Hvilken vagtplan vil du have? (aktuel/næste/) ")
        else:
            print("Forkert input skriv y/n")
            exit() 
    else:
        user_input_brugernavn = input("Indtast brugernavn ")
        user_input_adgangskode = input("Indtast adgangskode ")
        vagtplan = input("Hvilken vagtplan vil du have? (aktuel/næste/) ")
    # Skriver brugernavn og adgangskode til config filen
    with open("config.py", "w") as file:
        try:
            file.write(f"user_brugernavn = '{user_input_brugernavn}'\n")
            file.write(f"user_adgangskode = '{user_input_adgangskode}'\n")
        except: 
            print("error")

    # Tjekker hvilken vagtplan brugeren ønsker og gemmer det i en variabel der returnes når funktion er færdig
    if vagtplan == "næste":
        periode = "next"
    elif vagtplan == "aktuel":    
        periode = "current"  
    else: print("error")
    
    return periode



