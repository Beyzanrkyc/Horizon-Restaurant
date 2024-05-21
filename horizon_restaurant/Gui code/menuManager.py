# Authors: William Forber Student ID:22015706
# Lewis Quick, Student ID:22016949
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from main import *

font = ("Arial", 14)


class AddDish(tk.Frame):
    def __init__(self, container, callback, menu):
        super().__init__(container)
        # configuring the width of columns and rows
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.callback = callback
        self.menu = menu
        view = self.create_widgets()
        view.pack(fill='both', expand=True)

    def create_widgets(self):
        # loading the current user
        refresh_current_user()
        current_user = load_current_user()
        frame = ttk.Frame(self)
        display = {}
        name = tk.StringVar()
        price = tk.StringVar()
        time = tk.StringVar()
        display['name_label'] = ttk.Label(frame, text="Dish Name:", font=font)
        display['name_input'] = ttk.Entry(frame, textvariable=name, font=font)
        display['list_box_label'] = ttk.Label(frame, text="Ingredients For Dish:", font=font)
        display['list_box'] = tk.Listbox(frame, selectmode="multiple", font=font)
        display['price_label'] = ttk.Label(frame, text="Price For Dish:", font=font)
        display['price_input'] = ttk.Entry(frame, textvariable=price, font=font)
        display['time_label'] = ttk.Label(frame, text="Time To Cook (minutes):", font=font)
        display['time_input'] = ttk.Entry(frame, textvariable=time, font=font)
        display['addDish'] = ttk.Button(frame, text="Add Dish to Menu",
                                        command=lambda: self.begin_adding_dish(self.menu, name, price, time,
                                                                               display['list_box']))

        for inventory in current_user.get_restaurant().get_inventories():
            for ingredient in inventory.get_ingredients():
                display['list_box'].insert('end', ingredient.get_name())
        # displaying the list box
        for i in display.values():
            i.pack(fill='both', expand=True, pady=10, padx=10)
        return frame

    def refresh(self):
        refresh_current_user()
        for widget in self.winfo_children():
            widget.destroy()
        view = self.create_widgets()
        view.pack()

    def begin_adding_dish(self, menu, name, price, time, ingredients):
        name = name.get()
        price = price.get()
        time = time.get()
        if name:
            if check_input(price, True):
                if check_input(time):
                    if ingredients.curselection():
                        add_dish(name, menu[0], price, time, ingredients)
                        self.callback()
                        self.master.destroy()
                    else:
                        tkm.showerror("Ingredients needed!", "Ingredients are needed for a menu dish!")
                        return False
                else:
                    tkm.showerror("Time Invalid", "The time needs to be an integer!")
                    return False
            else:
                tkm.showerror("Price Invalid", "The price needs to be a valid number!")
                return False
        else:
            tkm.showerror("Name Needed!", "A dish name needs to be specified!")
            return False


class RmDish(tk.Frame):
    def __init__(self, container, callback, menu):
        super().__init__(container)
        # configuring the width of columns and rows
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.callback = callback
        self.menu = menu
        view = self.create_widgets()
        view.pack()

    def create_widgets(self):
        # loading the current user
        refresh_current_user()
        current_user = load_current_user()
        frame = ttk.Frame(self)
        display = {'list': ttk.Treeview(frame, column=("c1", "c2"), show='headings',
                                        selectmode="browse")}
        # defining the tree view which will display the orders
        display['list'].column("# 1")
        display['list'].heading("# 1", text="Dish ID")
        display['list'].column("# 2")
        display['list'].heading("# 2", text="Dish Name")
        # defining the buttons
        display['removeDish'] = ttk.Button(frame, text="Remove Dish",
                                           command=lambda: self.begin_removing_dish(display['list']))

        for menu in current_user.get_restaurant().get_menus():
            if int(self.menu[0]) == menu.get_menu_id():
                for dish in menu.get_dishes():
                    display['list'].insert('', 'end', text=dish.get_dish_id(),
                                           values=(str(dish.get_dish_id()), dish.get_name(),))

        # displaying the list box
        for i in display.values():
            i.pack(fill='both', expand=True, pady=10, padx=10)

        return frame

    def refresh(self):
        refresh_current_user()
        for widget in self.winfo_children():
            widget.destroy()
        view = self.create_widgets()
        view.pack()

    def begin_removing_dish(self, dish):
        if dish.selection():
            current_item = dish.focus()
            dish_details = dish.item(current_item, 'values')
            if askyesno("Delete this dish?", "Are you sure you want to remove this dish?"):
                remove_dish(int(dish_details[0]))
        else:
            tkm.showerror("Selection Needed!", "A dish needs to be selected in order to remove it!")
            return False
        self.callback()
        self.master.destroy()


class SetCategory(tk.Frame):
    def __init__(self, container, callback, menu):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.callback = callback
        self.menu = menu
        view = self.create_widgets()
        view.pack()

    def create_widgets(self):
        frame = ttk.Frame(self)
        catInput = tk.StringVar()
        display = {}
        display["cat"] = ttk.Label(frame, text="Enter Category:", font=font)
        display["catInput"] = ttk.Entry(frame, textvariable=catInput, font=font)
        display["submitButton"] = ttk.Button(frame, text="Submit",
                                             command=lambda: self.begin_cat_set(self.menu, catInput.get()))

        for i in display.values():
            i.pack(fill='both', expand=True, pady=10, padx=10)

        return frame

    def begin_cat_set(self, menu, cat_input):
        if cat_input:
            set_menu_category(menu[0], cat_input)
        else:
            tkm.showerror("Input Needed!", "Please input a category!")
            return False
        self.callback()
        self.master.destroy()


class AddMenu(tk.Frame):
    def __init__(self, container, callback):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.callback = callback
        view = self.create_widgets()
        view.pack()

    def create_widgets(self):
        frame = ttk.Frame(self)
        category = tk.StringVar()
        display = {}
        display["cat"] = ttk.Label(frame, text="Enter Category:", font=font)
        display["catInput"] = ttk.Entry(frame, textvariable=category, font=font)
        display["submitButton"] = ttk.Button(frame, text="Submit", command=lambda: self.begin_add_menu(category))

        for i in display.values():
            i.pack(fill='both', expand=True, pady=10, padx=10)

        return frame

    def begin_add_menu(self, category):
        category = category.get()
        if category:
            create_menu(category)
        else:
            tkm.showerror("Category Invalid!", "The category needs to be provided!")
            return False
        self.callback()
        self.master.destroy()
