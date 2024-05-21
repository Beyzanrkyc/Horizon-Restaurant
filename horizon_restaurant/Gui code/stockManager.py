# Author: William Forber, Student ID:22015706
import tkinter as tk
from tkinter import ttk
from main import *


class AddStock(tk.Frame):
    def __init__(self, container, inv_id, callback):
        super().__init__(container)
        self.inv_id = inv_id
        self.columnconfigure(0, weight=2)
        self.font = ("Arial", 14)
        self.name = tk.StringVar()
        self.quantity = tk.StringVar()
        self.callback = callback
        self.display = {'entry_label': ttk.Label(self, text="Add Stock:", font=self.font),
                        'name_input': ttk.Label(self, text="Ingredient Name:", font=self.font),
                        'ing_name': ttk.Entry(self, textvariable=self.name, font=self.font),
                        'quantity_input': ttk.Label(self, text="Quantity:", font=self.font),
                        'quantity': ttk.Entry(self, textvariable=self.quantity, font=self.font),
                        'add': ttk.Button(self, text="Add Ingredient", command=lambda: self.begin_add())}
        row = 0
        for to_display in self.display.values():
            to_display.grid(row=row, column=0, columnspan=2, pady=5, padx=5, sticky="ew")
            row += 1

    def begin_add(self):
        if check_input(self.quantity.get()):
            if self.name.get():
                add_ingredient(self.inv_id, self.name.get(), self.quantity.get())
                self.callback()
                self.master.destroy()
            else:
                tkm.showerror("Ingredient name invalid!", "A ingredient name needs to be provided!")
        else:
            tkm.showerror("Quantity invalid!", "The quantity can only be a integer!")


class UpdateStock(tk.Frame):
    def __init__(self, container, variables_to_pass, callback):
        super().__init__(container)
        refresh_current_user()
        self.current_user = load_current_user()
        self.font = ("Arial", 14)
        self.stock_name = variables_to_pass[0]
        self.inv_id = int(variables_to_pass[1])
        if not (search_ingredients(self.inv_id, self.stock_name)):
            tkm.showerror("Ingredient not found", "The ingredient was not found check spelling of ingredient!")
            self.master.destroy()
            return False
        self.ingredient = search_ingredients(self.inv_id, self.stock_name)
        self.input_name = tk.StringVar()
        self.prev_quantity = self.ingredient.get_quantity()
        self.quantity = tk.StringVar()
        self.callback = callback
        self.display = {'name_label': ttk.Label(self, text="Ingredient Name:", font=self.font),
                        'name_input': ttk.Entry(self, textvariable=self.input_name, font=self.font),
                        'quantity_label': ttk.Label(self, text="Quantity:", font=self.font),
                        'quantity_input': ttk.Entry(self, textvariable=self.quantity, font=self.font),
                        'button': ttk.Button(self, text="Update Stock", command=lambda: self.begin_update())}
        self.display['name_input'].insert(0, self.stock_name)
        self.display['quantity_input'].insert(0, self.prev_quantity)
        row = 0
        for to_display in self.display.values():
            to_display.grid(row=row, column=0, columnspan=2, sticky="ew", padx=50, pady=5)
            row += 1

    def begin_update(self):
        if not (check_input(self.quantity.get())):
            tkm.showerror("Quantity invalid!", "The quantity must be an integer")
            return False
        if not self.input_name:
            tkm.showerror("Name is invalid", "The name cannot be empty!")
            return False
        update_ingredient(self.ingredient.get_item_id(), self.input_name.get(), self.quantity.get())
        self.master.destroy()
        self.callback()


class StockViewer(tk.Frame):
    def __init__(self, container, inv_id, callback):
        super().__init__(container)
        self.font = ("Arial", 14)
        refresh_current_user()
        current_user = load_current_user()
        self.callback = callback
        self.inv_id = inv_id
        self.display = {'stock_tree': ttk.Treeview(self, column=("c1", "c2", "c3"), show='headings',
                                                   selectmode="browse")}
        self.display['stock_tree'].column("# 1")
        self.display['stock_tree'].heading("# 1", text="Item ID")
        self.display['stock_tree'].column("# 2")
        self.display['stock_tree'].heading("# 2", text="Ingredient Name")
        self.display['stock_tree'].column("# 3")
        self.display['stock_tree'].heading("# 3", text="Quantity")

        for inventory in current_user.get_restaurant().get_inventories():
            if inventory.get_inventory_id() == inv_id:
                for ingredient in inventory.get_ingredients():
                    self.display['stock_tree'].insert('', 'end', text=str(ingredient.get_item_id()),
                                                      values=(str(ingredient.get_item_id()),
                                                              ingredient.get_name(),
                                                              str(ingredient.get_quantity())))

        row = 0
        for display in self.display.values():
            display.grid(row=row, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
            row += 1


class ShowLowStock(tk.Frame):
    def __init__(self, container, stock, callback):
        super().__init__(container)
        self.font = ("Arial",14)
        self.callback = callback
        self.low_stock = stock
        self.display = ttk.Treeview(self, column=("c1", "c2", "c3"), show='headings', selectmode="browse")
        self.display.column('# 1')
        self.display.heading('# 1', text="Item ID")
        self.display.column('# 2')
        self.display.heading('# 2', text='Ingredient Name')
        self.display.column('# 3')
        self.display.heading('# 3', text="Quantity")
        self.label = ttk.Label(self, text="Current Items With Low Stock:", font=self.font)
        self.button = ttk.Button(self, text="Confirm", command=lambda: self.close())
        for ingredient in self.low_stock:
            self.display.insert('', 'end', text=str(ingredient.get_item_id()),
                                values=(str(ingredient.get_item_id()),
                                        ingredient.get_name(),
                                        str(ingredient.get_quantity())))
        self.label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.display.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.button.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

    def close(self):
        self.master.destroy()
