import tkinter as tk
from tkinter import ttk, messagebox
import os
import threading  # Importer threading for at køre baggrundsopgaver
#from Test import LoginSide  # Importer LoginSide


large_font = ("Verdana", 14)
frame_styles = {"relief": "groove",
                "bd": 3, "bg": "#BEB2A7",
                "fg": "#073bb3", "font": ("Arial", 9, "bold")}

background_style = {"bg": "#333333"}

title_style = {"bg": "#333333",
                "fg": "#0088FF",
                "font": ("Arial", 20, "bold")}

text_style = {"bg": "#333333",
                "fg": "#0088FF",
                "font": ("Arial", 16, "bold")}

button_style = {"bg": "#E6E6E6",
                "fg": "#0088FF",
                "font": ("Arial", 20, "bold")}

class MyGUI(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        
        tk.Tk.wm_title(self, "Vagtplan til ICS")
        main_frame = tk.Frame(self)
        self.geometry("800x600")
        main_frame.pack(fill="both", expand="true")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        self.frames={}

        for F in (Loginpage, page_one, page_two, page_three, page_four):
            frame = F(main_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        if os.path.exists('login.py'):
            self.show_frame(page_one)
        else:
            self.show_frame(Loginpage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# def login(param):
#             print("Login button clicked")
#             print(param)
#             controller.show_frame(page_one)
    
        

class Loginpage(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)

        self.configure(bg="#333333")

        # Konfigurer grid for centrering
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1) # Tilføj en tom række i bunden for centrering


        #Laver widgets til login siden
        login_label = tk.Label(self, text="Angiv dit login til hjemmesiden", **title_style )
        username_label = tk.Label(self, text="Brugernavn", **text_style)
        username_entry = ttk.Entry(self, width=35)
        password_label = tk.Label(self, text="Adgangskode", **text_style)
        password_entry = ttk.Entry(self, show="*", width=35)
        login_button = tk.Button(self, button_style, text="Login", command=lambda: login("test"))

        # Placerer widgets i vinduet med centrering
        login_label.grid(row=1, column=0, columnspan=2, pady=20) # 'columnspan=2' for at strække sig over begge kolonner
        username_label.grid(row=2, column=0, sticky="e", padx=5) # 'e' for højrejustering i cellen
        username_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5) # 'w' for venstrejustering i cellen
        password_label.grid(row=3, column=0, sticky="e", padx=5)
        password_entry.grid(row=3, column=1, sticky="w", padx=5, pady=10)
        login_button.grid(row=4, column=0, columnspan=2, pady=10)


        def login(param):
            username = "testuser"
            password = "1337"
            #print(username_entry.get())
            #password_entry.get()
            if username_entry.get() == username and password_entry.get() == password:
                print("Login successful")
                messagebox.showinfo("Login", "Login successful")
                with open("login.py", "w") as file:
                    try:
                        file.write(f"user_brugernavn = '{username_entry.get()}'\n")
                        file.write(f"user_adgangskode = '{password_entry.get()}'\n")
                    except: 
                        print("error")
            else:
                messagebox.showinfo("Login", "For at bruge mockupdata brug \nvenligst følgende oplysninger \nusername = testuser\npassword = 1337")

            # with open("login.py", "w") as file:
            #     try:
            #         file.write(f"user_brugernavn = '{username_entry.get()}'\n")
            #         file.write(f"user_adgangskode = '{password_entry.get()}'\n")
            #     except: 
            #         print("error")
            #print("Login button clicked")
            #print(param)
            controller.show_frame(page_two)
        #self.root.mainloop()
        #command=lambda: login("test")

class page_one(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        self.configure(bg="#333333")
        label = tk.Label(self, text="Vil du bruge dit tidligere login?", **title_style)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Ja", width=5, **button_style, command=lambda: controller.show_frame(page_two))
        button1.pack(pady=10, padx=10)
        button2 = tk.Button(self, text="Nej", width=5, **button_style, command=lambda: controller.show_frame(Loginpage))
        button2.pack(pady=10, padx=10)

        # label.pack(pady=10, padx=10)

        # label2 = tk.Label(self, text="Brugernavn")
        # label2.pack(pady=10, padx=10)
        # entry1 = ttk.Entry(self)
        # entry1.pack(pady=0, padx=10)

        # label3 = tk.Label(self, text="Adgangskode")
        # label3.pack(pady=10,padx=10)
        # entry2 = ttk.Entry(self, show="*")
        # entry2.pack(pady=0, padx=10)


        button1 = tk.Button(self, text="back", command=lambda: controller.show_frame(Loginpage))
        button1.pack(pady=10, padx=10)

        tk.Listbox

class page_two(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        self.configure(bg="#333333")
        label = tk.Label(self, text="Hvilken vagt plan skal konverteres?", **title_style)
        label.pack(pady=15, padx=10)

        vagtplan_combo = ttk.Combobox(self, 
                                    values=["Aktuel vagtplan", "Næste vagtplan"],
                                    font=button_style["font"])  # Brug font fra button_style
        vagtplan_combo.pack(pady=10, padx=10)
        vagtplan_combo.set("Vælg vagtplan")  # Standardvalg
        vagtplan_combo["state"] = "readonly"  # Gør det til en dropdown

        button_vaelg = tk.Button(self, text="Vælg", command=lambda: vaelg_vagtplan(), **button_style)  # Ændret command
        button_vaelg.pack(pady=10, padx=10)
        

        def vaelg_vagtplan():
            vagtplan = vagtplan_combo.get()
            print(f"Brugeren valgte: {vagtplan}")
            
            if vagtplan == "Næste vagtplan":
                periode = "next"
            elif vagtplan == "Aktuel vagtplan":    
                periode = "current"  
            else: print("error")
            
            with open("config.py", "w") as file:
                try:
                    file.write(f"valgt_vagtplan = '{periode}'\n")
                except: 
                    print("error")
            controller.show_frame(page_three)

            
        #print(periode)

            # if valgt_vagtplan == "Aktuel vagtplan":
            #     # Gør noget for 'Aktuel vagtplan'
            #     self.controller.show_frame(page_two)  # Eller en anden side
            # elif valgt_vagtplan == "Næste vagtplan":
            #     # Gør noget for 'Næste vagtplan'
            #     self.controller.show_frame(Loginpage)  # Eller en anden side
            # else:
            #     print("Ugyldigt valg")
class page_three(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#333333")
        label = tk.Label(self, text="Klar til at køre programmet", **title_style)
        label.pack(pady=15, padx=10)

        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=300, mode="indeterminate")
        self.progress_bar.pack(pady=10)
        
        self.status_text = tk.StringVar()
        self.status_label = tk.Label(self, textvariable=self.status_text, **text_style)
        self.status_label.pack(pady=10)

        self.start_process_button = tk.Button(self, text="Start program", command=self.start_process, **button_style)
        self.start_process_button.pack(pady=20)

    def start_process(self):
        self.progress_bar.start(10)  # Start progress bar animation
        self.start_process_button.config(state="disabled")  # Deaktiver knappen

        # Kør processen i en separat tråd for at undgå at fryse GUI'en
        threading.Thread(target=self.run_my_script).start()

    def run_my_script(self):
        # Her skal du importere og kalde din hovedscript-funktion
        from Main_copy import my_main_function  # Ændre dette
        my_main_function(self.update_status)  # Kald funktionen og send update_status
        self.after(0, self.process_complete)

    def update_status(self, message):
        # Opdater status-teksten i GUI'en (skal gøres fra hovedtråden)
        self.after(0, self.status_text.set, message)

    def process_complete(self):
        self.progress_bar.stop()
        self.status_text.set("Processen er fuldført!")
        self.start_process_button.config(state="normal")  # Genaktiver knappen
        self.controller.show_frame(page_four)

class page_four(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#333333")
        label = tk.Label(self, text="Kalender", **title_style)
        label.pack(pady=15, padx=10)

GUI = MyGUI()
#GUI.geometry("800x600")
#GUI.configure(bg="#333333")
GUI.mainloop()
