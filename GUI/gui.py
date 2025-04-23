import tkinter as tk
from tkinter import ttk
from Test import LoginSide  # Importer LoginSide


large_font = ("Verdana", 14)
frame_styles = {"relief": "groove",
                "bd": 3, "bg": "#BEB2A7",
                "fg": "#073bb3", "font": ("Arial", 9, "bold")}

background_style = {"bg": "#333333"}
text_style = {"bg": "#333333",
                "fg": "#0088FF",
                "font": ("Arial", 14, "bold")}

button_style = {"bg": "#E6E6E6",
                "fg": "#0088FF",
                "font": ("Arial", 14, "bold")}

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

        for F in (Loginpage, page_one):
            frame = F(main_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

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
        #Laver widgets til login siden
        login_label = tk.Label(self, text_style, text="Angiv dit login til hjemmesiden" )
        username_label = tk.Label(self, text_style, text="Brugernavn")
        username_entry = ttk.Entry(self)
        password_label = tk.Label(self, text_style, text="Adgangskode")
        password_entry = ttk.Entry(self, show="*")
        login_button = tk.Button(self, button_style, text="Login", command=lambda: login("test"))

        #Placerer widgets i vinduet
        login_label.grid(row=0, column=0, columnspan=2)
        username_label.grid(row=1, column=0)
        username_entry.grid(row=1, column=1)
        password_label.grid(row=2, column=0)
        password_entry.grid(row=2, column=1)
        login_button.grid(row=3, column=0, columnspan=2, pady=10)

        # label = tk.Label(self, text="Angiv dit login til hjemmesiden", font=large_font)
        # label.pack(pady=10, padx=10)

        # label2 = tk.Label(self, text="Brugernavn")
        # label2.pack(pady=10, padx=10)
        # entry1 = ttk.Entry(self)
        # entry1.pack(pady=0, padx=10)

        # label3 = tk.Label(self, text="Adgangskode")
        # label3.pack(pady=10,padx=10)
        # entry2 = ttk.Entry(self, show="*")
        # entry2.pack(pady=0, padx=10)


        # button1 = tk.Button(self, text="Login", command=lambda: login("test"))
        # button1.pack(pady=10, padx=10)


        def login(param):
           print("Login button clicked")
           print(param)
           controller.show_frame(page_one)
        #self.root.mainloop()
        #command=lambda: login("test")

class page_one(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Hvilken vagt plan skal konverteres?", font=large_font)
        label.pack(pady=10, padx=10)

        label2 = tk.Label(self, text="Brugernavn")
        label2.pack(pady=10, padx=10)
        entry1 = ttk.Entry(self)
        entry1.pack(pady=0, padx=10)

        label3 = tk.Label(self, text="Adgangskode")
        label3.pack(pady=10,padx=10)
        entry2 = ttk.Entry(self, show="*")
        entry2.pack(pady=0, padx=10)


        button1 = tk.Button(self, text="back", command=lambda: controller.show_frame(Loginpage))
        button1.pack(pady=10, padx=10)

        tk.Listbox

GUI = MyGUI()
#GUI.geometry("800x600")
#GUI.configure(bg="#333333")
GUI.mainloop()
