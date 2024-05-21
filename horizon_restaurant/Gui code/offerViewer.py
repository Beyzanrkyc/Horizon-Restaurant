# Authors: Zahin Hussain, Student ID: 22016373
# Lewis Quick, Student ID:22016949
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from main import *
from offerManager import *

font = ("Arial", 14)


# creating an order viewer frame
class OfferManagement(tk.Frame):
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
        display['list'] = ttk.Treeview(frame, column=("c1", "c2", "c3"), show='headings',
                                       selectmode="browse")
        display['list'].column("# 1")
        display['list'].heading("# 1", text="Discount ID")
        display['list'].column("# 2")
        display['list'].heading("# 2", text="Discount")
        display['list'].column("# 3")
        display['list'].heading("# 3", text="Menu Dish")

        y_scrollbar = ttk.Scrollbar(self, orient="vertical", command=display['list'].yview)
        display['list'].configure(yscrollcommand=y_scrollbar.set)
        y_scrollbar.pack(side="right", fill="y")

        # defining the buttons
        display['addOff'] = ttk.Button(frame, text="Add Offer",
                                        command=lambda: self.open_new_window(AddOffer, "Add Offer", self.refresh))
        display['rmOff'] = ttk.Button(frame, text="Remove Offer",
                                       command=lambda: self.begin_delete(display['list']))

        for offer in offer_list:
            offer_id = offer.get_offer_id()
            display['list'].insert('', 'end', text="ID ",
                                   values=(str(offer_id),
                                           offer.get_offer(), offer.get_menu_dish_id))

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

    def begin_offer_add(self, offer):
        if not (offer.selection()):
            tkm.showerror("Selection needed!", "You need to select an offer!")
            return False
        self.open_new_window(AddOffer, "Add Offer", self.refresh, offer)

    def begin_delete(self, offer):
        current_item = offer.focus()
        details = offer.item(current_item, 'values')
        if not details:
            tkm.showerror("Selection needed", "An offer needs to be selected before it can be deleted")
            return False
        if askyesno("Delete this offer?", "Are you sure you want to delete this offer?"):
            remove_offer(int(details[0]))
            self.refresh()

    def open_new_window(self, root, title, callback, offer=None):
        new_window = tk.Toplevel(self)
        new_window.title(title)
        new_window.resizable(0, 0)
        if offer is not None:
            current_item = offer.focus()
            offer_details = offer.item(current_item, 'values')
            new_frame = root(new_window, callback, offer_details)
        else:
            new_frame = root(new_window, callback)
        new_frame.pack()
        new_window.wait_window()
