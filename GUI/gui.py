import tkinter as tk
from tkinter import ttk

large_font = ("Verdana", 12)


class MyGUI(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)

        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand="true")

        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        self.frames={}

        frame = Loginpage(main_frame, self)

        self.frames[Loginpage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Loginpage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


        

class Loginpage(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Login", font=large_font)
        label.pack(pady=10, padx=10)

        #self.root.mainloop()


GUI = MyGUI()
GUI.mainloop()
