# Author: William Forber, Student ID: 22015706
import tkinter as tk
from tkinter import ttk
from main import *

titleFont = ("Arial", 16)
contentFont = ("Arial", 14)

# creating a window class
class AddOrderGui(tk.Tk):
    def __init__(self):
        super().__init__()
        # defining the window size and making the window not resizable
        self.title("Add order")
        self.geometry("500x360")
        self.resizable(0, 0)
        # adding widgets to the window
        self.create_widgets()
        # configuring the columns on the window
        self.columnconfigure(0, weight=3)

    # function adding widgets to the window
    def create_widgets(self):
        currentUser = load_current_user()
        menu_dish_display = {}
        menu_dish_display['Label'] = ttk.Label(text="Order contents:", font=titleFont)
        menu_dish_display['list'] = tk.Listbox(self, selectmode="multiple", font=contentFont)
        for menu in currentUser.get_restaurant().get_menus():
            for dish in menu.get_dishes():
                menu_dish_display['list'].insert('end', dish.get_name())

        menu_dish_display['Add dish'] = ttk.Button(text="Add order",
                                                   command=lambda: self.begin_adding(menu_dish_display['list']))
        index = 0
        # displaying the widgets on the window
        for display in menu_dish_display.values():
            display.grid(row=index, padx=10, pady=10, column=0, columnspan=2, sticky="ew")
            index += 1

    def begin_adding(self, menu_dishes):
        add_order(menu_dishes)
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()




initialize_objects(1)
app = AddOrderGui()
app.mainloop()
