import os
import json

def write_json(new_data, filename='data.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["tillaeg"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

def setup():
    list = []
    USER_INPUT = None
    if os.path.exists('config.py'): #check if config file exist
        ask = input("Vil du bruge gemt brugernavn/adgangskode? (y/n) ")
        if ask == "n":
            user_input_brugernavn = input("Indtast brugernavn ")
            user_input_adgangskode = input("Indtast adgangskode ")
            vagtplan = input("Hvilken vagtplan vil du have? (aktuel/næste/forrige) ")
        elif ask == 'y':
            import config
            user_input_brugernavn = config.user_brugernavn
            user_input_adgangskode = config.user_adgangskode
            vagtplan = input("Hvilken vagtplan vil du have? (aktuel/næste/forrige) ")
        else:
            print("Forkert input skriv y/n")
            exit() 
    else:
        user_input_brugernavn = input("Indtast brugernavn ")
        user_input_adgangskode = input("Indtast adgangskode ")
        vagtplan = input("Hvilken vagtplan vil du have? (aktuel/næste/forrige) ")

    with open("config.py", "w") as file:
        try:
            file.write(f"user_brugernavn = '{user_input_brugernavn}'\n")
            file.write(f"user_adgangskode = '{user_input_adgangskode}'\n")
        except: 
            print("error")

    #print(type(vagtplan))

    if vagtplan == "næste":
        periode = "Næste planlægningsperiode"
        #print(periode)
    elif vagtplan == "aktuel":    
        periode = "Nuværende planlægningsperiode"
        #print(periode)
    elif vagtplan == "forrige":    
        periode = "Tidligere planlægningsperiode"
        #print(periode)    
    else: print("error")
    
    
    return periode



