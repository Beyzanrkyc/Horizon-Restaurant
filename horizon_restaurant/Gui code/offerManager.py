# Authors: Zahin Hussain, Student ID: 22016373
# Lewis Quick, Student ID:22016949
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from main import *

font = ("Arial", 14)


class AddOffer(tk.Frame):
    def __init__(self, container, callback):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.callback = callback
        view = self.create_widgets()
        view.pack()

    def create_widgets(self):
        frame = ttk.Frame(self)
        discount = tk.StringVar()
        display = {}
        display["discount"] = ttk.Label(frame, text="Enter Discount:", font=font)
        display["discInput"] = ttk.Entry(frame, textvariable=discount, font=font)
        display['list_box_label'] = ttk.Label(frame, text="Menu Dishes:", font=font)
        display['list_box'] = tk.Listbox(frame, selectmode="single", font=font)
        display["submitButton"] = ttk.Button(frame, text="Submit", command=lambda: self.begin_add_offer(discount, display['list_box']))

        for dish in menu_dish_list:
            display['list_box'].insert('end', dish.get_name())
        
        for i in display.values():
            i.pack(fill='both', expand=True, pady=10, padx=10)

        return frame

    def begin_add_offer(self, discount, dish):
        discount = discount.get()
        dish = dish.curseselection()
        if discount:
            if dish:
                create_offer(discount, dish)
            else:
                tkm.showerror("Offer Invalid!", "The dish needs to be provided!")
        else:
            tkm.showerror("Discount Invalid!", "The discount needs to be provided!")
            return False
        self.callback()
        self.master.destroy()
