# Author: William Forber, Student ID: 22015706
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from main import *
from tableManager import AddTable, UpdateTable

font = ("Arial", 14)


# creating an order viewer frame
class TableViewer(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        # configuring the width of columns and rows
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        order_view = self.create_widgets()
        order_view.pack()

    def create_widgets(self):
        # loading the current user
        current_user = load_current_user()
        table_frame = ttk.Frame(self)
        table_display = {}
        buttons = {}
        # defining the tree view which will display the orders
        table_display['list'] = ttk.Treeview(table_frame, column=("c1", "c2"), show='headings',
                                             selectmode="browse")
        table_display['list'].column("# 1")
        table_display['list'].heading("# 1", text="Table Number")
        table_display['list'].column("# 2")
        table_display['list'].heading("# 2", text="Table Capacity")

        y_scrollbar = ttk.Scrollbar(self, orient="vertical", command=table_display['list'].yview)
        table_display['list'].configure(yscrollcommand=y_scrollbar.set)
        y_scrollbar.pack(side="right", fill="y")

        # defining the buttons
        buttons['add'] = ttk.Button(table_frame, text="Add Table ", width=45,
                                    command=lambda: self.open_new_window(AddTable, "Add Table", self.refresh))

        buttons['update'] = ttk.Button(table_frame, text="Update Table", width=45,
                                       command=lambda: self.open_new_window(UpdateTable, "Update Table", self.refresh,
                                                                            table_display['list']))

        buttons['delete'] = ttk.Button(table_frame, text="Delete Table", width=45,
                                       command=lambda: self.begin_delete(table_display))

        for table in current_user.get_restaurant().get_tables():
            table_display['list'].insert('', 'end', text=str(table.get_table_number()),
                                         values=(str(table.get_table_number()),
                                                 str(table.get_capacity())))

        index = 2
        # displaying the list box
        for display in table_display.values():
            display.pack(fill='both', expand=True, pady=10, padx=10)
            index += 1

        # displaying the buttons
        for button in buttons.values():
            button.pack(pady=5, padx=5)
            index += 1
        return table_frame

    def refresh(self):
        refresh_current_user()
        for widget in self.winfo_children():
            widget.destroy()
        table_view = self.create_widgets()
        table_view.pack()

    def begin_delete(self, table_display):
        current_item = table_display['list'].focus()
        table_details = table_display['list'].item(current_item, 'values')
        if not table_details:
            tkm.showerror("Selection needed", "An order needs to be selected before it can be deleted")
            return False
        if askyesno("Delete this order?", "Are you sure you want to delete this order?"):
            delete_table(table_details[0])
            self.refresh()

    def open_new_window(self, root, title, callback, table=None):
        new_window = tk.Toplevel(self)
        new_window.title(title)
        if table is not None:
            current_item = table.focus()
            table_details = table.item(current_item, 'values')
            new_frame = root(new_window, callback, table_details)
        else:
            new_frame = root(new_window, callback)
        new_frame.pack()
        new_window.wait_window()
