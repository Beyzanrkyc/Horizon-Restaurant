# Author: William Forber, Student ID: 22015706
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from main import *

font = ("Arial", 14)


# creating an order viewer frame
class OrderViewer(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        # configuring the width of columns and rows
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        order_view = self.create_widgets()
        order_view.pack()

    def create_widgets(self):
        # loading the current user
        refresh_current_user()
        current_user = load_current_user()
        initialize_objects()
        order_frame = ttk.Frame(self)
        order_display = {}
        buttons = {}
        # defining input variables
        price = tk.StringVar()
        time_placed = tk.StringVar()
        time_complete = tk.StringVar()
        status = tk.StringVar()
        # defining the tree view which will display the orders
        order_display['list'] = ttk.Treeview(order_frame, column=("c1", "c2", "c3", "c4", "c5"), show='headings',
                                             selectmode="browse")
        order_display['list'].column("# 1")
        order_display['list'].heading("# 1", text="Order ID")
        order_display['list'].column("# 2")
        order_display['list'].heading("# 2", text="Order Price")
        order_display['list'].column("# 3")
        order_display['list'].heading("# 3", text="Time Placed")
        order_display['list'].column("# 4")
        order_display['list'].heading("# 4", text="Estimated Complete Time")
        order_display['list'].column("# 5")
        order_display['list'].heading("# 5", text="Order Status")

        yscrollbar = ttk.Scrollbar(order_frame, orient="vertical", command=order_display['list'].yview)
        order_display['list'].configure(yscrollcommand=yscrollbar.set)
        yscrollbar.pack(side="right", fill="y")

        # defining the buttons
        buttons['add'] = ttk.Button(order_frame, text="Add order ", width=45, command=lambda: open_add_order_gui(self))

        buttons['update'] = ttk.Button(order_frame, text="Update order", width=45,
                                       command=lambda: self.show_input(buttons, order_display,
                                                                       price, time_placed, time_complete,
                                                                       status).pack())

        buttons['delete'] = ttk.Button(order_frame, text="Delete order", width=45,
                                       command=lambda: self.delete_choice(order_display))

        buttons['content'] = ttk.Button(order_frame, text="View order contents", width=45,
                                        command=lambda: self.open_new_window(ViewContents, "View Contents",
                                                                             order_display['list']))

        # for every order get the order contents and add that order to the treeview
        for order in current_user.get_restaurant().get_orders():
            order_display['list'].insert('', 'end', text=str(order.get_order_id()),
                                         values=(str(order.get_order_id()),
                                                 str(order.get_price()),
                                                 str(order.get_order_start()),
                                                 str(order.get_order_estend()),
                                                 order.get_order_status(),))

        # displaying the list box
        for display in order_display.values():
            display.pack(fill='both', expand=True, pady=10, padx=10)

        # displaying the buttons
        for button in buttons.values():
            button.pack(pady=5, padx=5)
        return order_frame

    # function disabling add, remove buttons and changing the update button
    def show_input(self, buttons, order_display, price, time_placed, time_complete, status):
        order_commands = ttk.Frame(self)
        order_commands.columnconfigure(0, weight=2)
        # defining the labels
        labels = {'price': ttk.Label(order_commands, text="Order Price:"),
                  'time_placed': ttk.Label(order_commands, text="Time Placed:"),
                  'estimated_complete': ttk.Label(order_commands, text="Estimated Complete Time:"),
                  'status': ttk.Label(order_commands, text="Order Status:")}
        # defining the text inputs
        order_input = {
            'price': ttk.Entry(order_commands, width=50, textvariable=price),
            'time_placed': ttk.Entry(order_commands, width=50, textvariable=time_placed),
            'estimated_complete': ttk.Entry(order_commands, width=50, textvariable=time_complete),
            'status': ttk.Entry(order_commands, width=50, textvariable=status)
        }

        current_item = order_display['list'].focus()
        # if no item in the tree view is selected output an error message
        if not current_item:
            tkm.showerror("Order needs to be selected:",
                          "The desired order needs to be selected before it can be modified!")
            return False

        buttons['add'].pack_forget()
        buttons['delete'].pack_forget()
        buttons['update'].pack_forget()

        # Get order details for the selected item
        order_details = order_display['list'].item(current_item, 'values')

        # Display labels on top of entries
        row = 4
        for label in labels.values():
            label.grid(row=row)
            row += 2
        row = 5
        for order_entry in order_input.values():
            order_entry.grid(row=row)
            row += 2

        # Populate entry widgets with order details
        order_input['price'].insert(0, order_details[1])
        order_input['time_placed'].insert(0, order_details[2])
        order_input['estimated_complete'].insert(0, order_details[3])
        order_input['status'].insert(0, order_details[4])

        # Add update button
        buttons['update'] = ttk.Button(order_commands, text="Update Order",
                                       command=lambda: self.begin_order_update(order_details, price.get(),
                                                                               time_placed.get(), time_complete.get(),
                                                                               status.get()))

        buttons['update'].grid(pady=20)

        return order_commands

    # function calling the update order in the main class
    def begin_order_update(self, order_details, price, time_placed, time_complete, status):
        if check_input(price, True):
            update_order(order_details, price, time_placed, time_complete, status)
        else:
            tkm.showerror("Invalid Price!", "The price inputted must not contain letters")
            return False
        self.refresh()

    # function refreshing the contents in the tree view
    def refresh(self):
        refresh_current_user()
        for widget in self.winfo_children():
            widget.destroy()
        order_view = self.create_widgets()
        order_view.pack()

    # function for deleting orders
    def delete_choice(self, order_display):
        current_item = order_display['list'].focus()
        order_details = order_display['list'].item(current_item, 'values')
        if not order_details:
            tkm.showerror("Selection needed", "An order needs to be selected before it can be deleted")
            return False
        if askyesno("Delete this order?", "Are you sure you want to delete this order?"):
            delete_order(order_details)
            self.refresh()

    def open_new_window(self, root, title, order):
        new_window = tk.Toplevel(self)
        new_window.title(title)
        if order.selection():
            current_item = order.focus()
            order_details = order.item(current_item, 'values')
            new_frame = root(new_window, int(order_details[0]))
        new_frame.pack()
        new_window.wait_window()


class ViewContents(tk.Frame):
    def __init__(self, container, order_id):
        super().__init__(container)
        self.order_id = order_id
        refresh_current_user()
        self.current_user = load_current_user()
        self.display = {'label': ttk.Label(self, text="Order Contents:", font=font),
                        'contents': tk.Listbox(self, font=font),
                        'button': ttk.Button(self, text="Ok", command=lambda: self.master.destroy())}

        for order in self.current_user.get_restaurant().get_orders():
            if order.get_order_id() == order_id:
                for dish in order.get_dishes():
                    self.display['contents'].insert('end', dish.get_name())

        row = 0
        for display in self.display.values():
            display.grid(row=row, column=0, columnspan=2, sticky="ew")
            row += 1
