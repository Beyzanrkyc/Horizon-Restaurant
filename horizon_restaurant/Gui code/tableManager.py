# Author: William Forber, Student ID: 22015706
import tkinter as tk
from tkinter import ttk
from main import *


class AddTable(tk.Frame):
    def __init__(self, container, callback):
        super().__init__(container)
        self.callback = callback
        self.font = ("Arial", 14)
        self.capacity = tk.StringVar()
        self.add_display = {'Title': ttk.Label(self, text="Table Capacity:", font=self.font),
                            'Capacity': ttk.Entry(self, textvariable=self.capacity, font=self.font),
                            'Button': ttk.Button(self, text="Add Table",
                                                 command=lambda: self.begin_adding(self.capacity.get()))}
        row = 0
        for display in self.add_display.values():
            display.grid(row=row, column=0, columnspan=2, pady=5, padx=5)
            row += 1

    def begin_adding(self, capacity):
        if check_input(capacity):
            capacity = int(capacity)
            add_table(capacity)
        else:
            tkm.showerror("Invalid Capacity", "The inputted capacity must not contain letters!")
            return False
        self.callback()
        self.master.destroy()


class UpdateTable(AddTable):
    def __init__(self, container, callback, table_details):
        super().__init__(container, callback)
        self.add_display['Capacity'].insert(0, int(table_details[1]))
        self.add_display['Button'].grid_forget()
        self.add_display['Button'] = ttk.Button(self, text="Update Table",
                                                command=lambda: self.begin_updating(table_details, self.capacity.get()))
        self.add_display['Button'].grid(row=2, column=0, columnspan=2, pady=5, padx=5)

    def begin_updating(self, table_details, capacity):
        if check_input(capacity):
            update_table(table_details, capacity)
        else:
            tkm.showerror("Invalid Capacity", "The inputted capacity must not contain letters!")
            return False
        self.callback()
        self.master.destroy()
