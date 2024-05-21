# Author Lewis Quick, Student ID:22016949
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from main import *
from menuManager import *

font = ("Arial", 14)


# creating an order viewer frame
class MenuManagement(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        # configuring the width of columns and rows
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        view = self.create_widgets()
        view.pack(fill='both', expand=True, padx=100)

    def create_widgets(self):
        # loading the current user
        refresh_current_user()
        current_user = load_current_user()
        frame = ttk.Frame(self)
        display = {}

        # defining the tree view which will display the menus
        display['list'] = ttk.Treeview(frame, column=("c1", "c2"), show='headings',
                                       selectmode="browse")
        display['list'].column("# 1")
        display['list'].heading("# 1", text="Menu ID")
        display['list'].column("# 2")
        display['list'].heading("# 2", text="Category")

        y_scrollbar = ttk.Scrollbar(self, orient="vertical", command=display['list'].yview)
        display['list'].configure(yscrollcommand=y_scrollbar.set)
        y_scrollbar.pack(side="right", fill="y")

        # defining the buttons
        display['addDish'] = ttk.Button(frame, text="Add Dish to Menu",
                                        command=lambda: self.begin_dish_add(display['list']))
        display['rmDish'] = ttk.Button(frame, text="Remove Dish from Menu",
                                       command=lambda: self.begin_dish_remove(display['list']))
        display['setCategory'] = ttk.Button(frame, text="Set Menu Category",
                                            command=lambda: self.begin_category_update(display['list']))
        display['addMenu'] = ttk.Button(frame, text="Add Menu", command=lambda: self.open_new_window(AddMenu,
                                                                                                     "Add Menu",
                                                                                                     self.refresh))
        display['rmMenu'] = ttk.Button(frame, text="Remove Menu", command=lambda: self.begin_delete(display['list']))

        for menu in current_user.get_restaurant().get_menus():
            menu_id = menu.get_menu_id()
            display['list'].insert('', 'end', text="ID ",
                                   values=(str(menu_id),
                                           menu.get_category()))

        # displaying the list box
        for i in display.values():
            i.pack(fill='both', expand=True, pady=10, padx=10)

        return frame

    def refresh(self):
        refresh_current_user()
        for widget in self.winfo_children():
            widget.destroy()
        view = self.create_widgets()
        view.pack(fill='both', expand=True, padx=100)

    def begin_dish_add(self, menu):
        if not (menu.selection()):
            tkm.showerror("Selection needed!", "You need to select a menu!")
            return False
        self.open_new_window(AddDish, "Add Dish", self.refresh, menu)

    def begin_dish_remove(self, menu):
        if not (menu.selection()):
            tkm.showerror("Selection needed!", "You need to select a menu!")
            return False
        self.open_new_window(RmDish, "Remove Dish", self.refresh, menu)

    def begin_category_update(self, menu):
        if not (menu.selection()):
            tkm.showerror("Selection needed!", "You need to select a menu!")
            return False
        self.open_new_window(SetCategory, "Update Menu Category", self.refresh, menu)

    def begin_delete(self, menu):
        current_item = menu.focus()
        details = menu.item(current_item, 'values')
        if not details:
            tkm.showerror("Selection needed", "A menu needs to be selected before it can be deleted")
            return False
        if askyesno("Delete this menu?", "Are you sure you want to delete this menu?"):
            remove_menu(int(details[0]))
            self.refresh()

    def open_new_window(self, root, title, callback, menu=None):
        new_window = tk.Toplevel(self)
        new_window.title(title)
        new_window.resizable(0, 0)
        if menu is not None:
            current_item = menu.focus()
            menu_details = menu.item(current_item, 'values')
            new_frame = root(new_window, callback, menu_details)
        else:
            new_frame = root(new_window, callback)
        new_frame.pack()
        new_window.wait_window()
