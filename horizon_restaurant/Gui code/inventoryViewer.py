# Author: Beyzanur Kayaci Student ID:22066921
import tkinter as tk
from tkinter import ttk
from main import *
from stockManager import AddStock, StockViewer, UpdateStock, ShowLowStock
from tkinter.messagebox import askyesno


class InventoryViewer(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.current_user = None
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.create_tree_widget()

    def create_tree_widget(self):
        tree_frame = ttk.Frame(self)
        self.tree = ttk.Treeview(tree_frame, column=("c1", "c2", "c3"), show='headings', selectmode="browse")
        refresh_current_user()
        self.current_user = load_current_user()
        # Define headings
        self.tree.column('# 1')
        self.tree.heading('# 1', text="Inventory Id")
        self.tree.column('# 2')
        self.tree.heading('# 2', text='Inventory Name')
        self.tree.column('# 3')
        self.tree.heading('# 3', text="Number Of Ingredients")

        self.tree.pack()

        for inventory in self.current_user.get_restaurant().get_inventories():
            if inventory.get_ingredients() is None:
                self.tree.insert('', 'end', text=str(inventory.get_inventory_id()),
                                 values=(str(inventory.get_inventory_id())
                                         , str(inventory.get_inventory_name()),
                                         "0"))
            else:
                self.tree.insert('', 'end', text=str(inventory.get_inventory_id()),
                                 values=(str(inventory.get_inventory_id())
                                         , str(inventory.get_inventory_name()),
                                         str(len(inventory.get_ingredients()))))

        left_frame = self.create_left_frame()
        right_frame = self.create_right_frame()

        tree_frame.pack(pady=5)
        left_frame.pack(side=tk.LEFT, padx=5)
        right_frame.pack(side=tk.RIGHT, padx=5)

    def create_left_frame(self):
        left_frame = tk.Frame(self)

        left_frame.rowconfigure(0, weight=6)
        left_frame.columnconfigure(0, weight=1)
        left_frame.columnconfigure(1, weight=1)

        tk.Label(left_frame, text='Name: ').grid(row=0, column=0, sticky=tk.E)
        self.name_entry = tk.Entry(left_frame, width=30)
        self.name_entry.focus()
        self.name_entry.grid(row=0, column=1, sticky=tk.W, padx=5)

        return left_frame

    def create_right_frame(self):
        right_frame = tk.Frame(self)

        right_frame.columnconfigure(0, weight=6)

        add_button = tk.Button(right_frame, text='Add Stock', command=lambda: self.add_stock(), width=35, height=2)
        add_button.grid(row=0, column=0, pady=5)

        delete_button = tk.Button(right_frame, text='Delete Stock', command=lambda: self.delete_stock(), width=35,
                                  height=2)
        delete_button.grid(row=1, column=0, pady=5)

        update_button = tk.Button(right_frame, text='Update Stock', command=lambda: self.update_stock(), width=35,
                                  height=2)
        update_button.grid(row=2, column=0, pady=5)

        check_button = tk.Button(right_frame, text='Check Stock', command=lambda: self.check_stock(), width=35,
                                 height=2)
        check_button.grid(row=3, column=0, pady=5)

        view_button = tk.Button(right_frame, text='View Stock', command=lambda: self.view_stock(), width=35, height=2)

        view_button.grid(row=4, column=0, pady=5)

        add_inventory_button = tk.Button(right_frame, text='Add Inventory', command=lambda: self.begin_add_inventory(),
                                         width=35, height=2)
        add_inventory_button.grid(row=5, column=0, pady=5)

        delete_inventory_button = tk.Button(right_frame, text='Delete Inventory', width=35, height=2,
                                            command=lambda: self.begin_delete_inventory())
        delete_inventory_button.grid(row=6, column=0, pady=5)

        return right_frame

    def refresh(self):
        refresh_current_user()
        self.current_user = load_current_user()
        for widget in self.winfo_children():
            widget.destroy()
        self.create_tree_widget()

    def add_stock(self):
        if not (self.tree.selection()):
            tkm.showerror("Selection needed!", "You need to select an inventory!")
            return False
        current_item = self.tree.focus()
        inv_details = self.tree.item(current_item, 'values')
        inv_id = inv_details[0]
        self.open_new_window(AddStock, "Add stock", self.refresh, inv_id)

    def delete_stock(self):
        if not (self.tree.selection()):
            tkm.showerror("Selection needed!", "You need to select an inventory!")
            return False
        stock_name = self.name_entry.get()
        if not stock_name:
            tkm.showerror("Name not inputted!",
                          "Please view stock items and type in the name of the stock item to update!")
            return False
        current_item = self.tree.focus()
        inv_details = self.tree.item(current_item, 'values')
        inv_id = inv_details[0]
        if not search_ingredients(int(inv_id), stock_name):
            tkm.showerror("Ingredient name incorrect!",
                          "The inputted ingredient name is not valid please check spelling!")
            return False
        if askyesno("Delete this ingredient", "Are you sure you want to delete this ingredient?"):
            delete_ingredient(stock_name)
            self.refresh()

    def update_stock(self):
        if not (self.tree.selection()):
            tkm.showerror("Selection needed!", "You need to select an inventory!")
            return False
        current_item = self.tree.focus()
        inv_details = self.tree.item(current_item, 'values')
        inv_id = inv_details[0]
        stock_name = self.name_entry.get()
        if not stock_name:
            tkm.showerror("Name not inputted!",
                          "Please view stock items and type in the name of the stock item to update!")
            return False
        variables_to_pass = [stock_name, inv_id]
        self.open_new_window(UpdateStock, "Update Stock", self.refresh, variables_to_pass)

    def check_stock(self):
        if not (self.tree.selection()):
            tkm.showerror("Selection needed!", "You need to select an inventory!")
            return False
        current_item = self.tree.focus()
        inv_details = self.tree.item(current_item, 'values')
        inv_id = inv_details[0]
        stock_name = self.name_entry.get()
        if not stock_name:
            stock_name = None
        if not search_ingredients(int(inv_id), stock_name) and stock_name is not None:
            tkm.showerror("Ingredient name incorrect!",
                          "The inputted ingredient name is not valid please view the stock and or check your spelling!")
            return False
        low_stock = check_stock(inv_id, stock_name)
        if low_stock:
            self.open_new_window(ShowLowStock, "Current Low Stock", self.refresh, low_stock)

    def view_stock(self):
        if not (self.tree.selection()):
            tkm.showerror("Selection needed!", "You need to select an inventory!")
            return False
        current_item = self.tree.focus()
        inv_details = self.tree.item(current_item, 'values')
        inv_id = inv_details[0]
        self.open_new_window(StockViewer, "Stock Viewer", self.refresh, int(inv_id))

    def begin_add_inventory(self):
        inventory_name = self.name_entry.get()
        if not inventory_name:
            tkm.showerror("Name needed", "The name of the inventory needs to be provided!")
            return False
        add_inventory(inventory_name)
        self.refresh()

    def open_new_window(self, root, title, callback, variable_to_pass):
        if not (self.tree.selection()):
            tkm.showerror("Selection needed!", "You need to select an inventory!")
            return False
        new_window = tk.Toplevel(self)
        new_window.title(title)
        new_frame = root(new_window, variable_to_pass, callback)
        new_frame.pack()
        new_window.wait_window()

    def begin_delete_inventory(self):
        inventory_name = self.name_entry.get()
        found = False
        if not inventory_name:
            tkm.showerror("Name needed", "The name of the inventory needs to be provided!")
            return False
        for inventory in self.current_user.get_restaurant().get_inventories():
            if inventory.get_inventory_name() == inventory_name:
                found = True
        if found:
            if askyesno("Delete Inventory?", "Are you sure you want to delete this inventory?"):
                delete_inventory(inventory_name)
        else:
            tkm.showerror("Inventory not found!", "Inventory not found! Please check your spelling!")
            return False
            self.refresh()
