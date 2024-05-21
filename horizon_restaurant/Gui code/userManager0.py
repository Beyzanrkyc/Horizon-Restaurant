# Author: Lewis Quick , Student ID: 22016949
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from main import *
from userManager import *

font = ("Arial", 14)


# creating an order viewer frame
class UserManagement(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        # configuring the width of columns and rows
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        view = self.create_widgets()
        view.pack()

    def create_widgets(self):
        # loading the current user
        current_user = load_current_user()
        frame = ttk.Frame(self)
        display = {}
        
        # defining the tree view which will display the orders
        display['list'] = ttk.Treeview(frame, column=("c1", "c2"), show='headings',
                                             selectmode="browse")
        display['list'].column("# 1")
        display['list'].heading("# 1", text="Username")
        display['list'].column("# 2")
        display['list'].heading("# 2", text="Restaurant")
        # defining the buttons
        display['chngUser'] = ttk.Button(frame, text="Change Username", command=lambda: self.open_new_window(ChngUser,
                                        "Change Username", self.refresh,display['list']))
        display['chngPswd'] = ttk.Button(frame, text="Change Password", command=lambda: self.open_new_window(ChngPswd,
                                        "Change Password", self.refresh,display['list']))
        display['chngPriv'] = ttk.Button(frame, text="Change Privilege", command=lambda: self.open_new_window(ChngPriv,
                                        "Change Privilege Category", self.refresh,display['list']))
        display['chngRest'] = ttk.Button(frame, text="Change Restaurant", command=lambda: self.open_new_window(ChngRest,
                                        "Change Restaurant", self.refresh,display['list']))
        display['del'] = ttk.Button(frame, text="Delete User", command=lambda: self.begin_delete(
                                        "Delete User", self.refresh,display['list']))
        display['del'] = ttk.Button(frame, text="Add User", command=lambda: self.open_new_window(AddUser,
                                        "Add User", self.refresh))

        for user in user_list:
            username = user.get_user_name()
            rest = user.get_restaurant()
            try:
                rest_name = rest.get_restaurant_name()
            except:
                rest_name = "void"
            display['list'].insert('', 'end', text="ID ",
                                         values=(str(username), str(rest_name)))

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

    def begin_delete(self, display):
        current_item = display['list'].focus()
        details = display['list'].item(current_item, 'values')
        if not details:
            tkm.showerror("Selection needed", "A user needs to be selected before it can be deleted")
            return False
        if askyesno("Delete this user?", "Are you sure you want to delete this user?"):
            remove_menu(details[0])
            self.refresh()


    def open_new_window(self, root, title, callback, user = None):
        new_window = tk.Toplevel(self)
        new_window.title(title)
        if user is not None:
            current_item = user.focus()
            details = user.item(current_item,'values')
            details = details[0]
            new_frame = root(new_window, callback, details)
        else:
            new_frame = root(new_window, callback)
        new_frame.pack()
        new_window.wait_window()

