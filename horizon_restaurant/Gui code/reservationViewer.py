#Author: Zahin Hussain, Student ID: 22016373
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from main import *
from reservationManager import ReservationsAdd, ReservationsUpdate

font = ("Arial", 14)


# creating an order viewer frame
class ReservationViewer(tk.Frame):
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
        initialize_objects(1)
        reservation_frame = ttk.Frame(self)
        reservation_display = {}
        buttons = {}
        # defining the tree view which will display the orders
        reservation_display['list'] = ttk.Treeview(reservation_frame, column=("c1", "c2", "c3", "c4", "c5"),
                                                   show='headings',
                                                   selectmode="browse")
        reservation_display['list'].column("# 1")
        reservation_display['list'].heading("# 1", text="Reservation ID")
        reservation_display['list'].column("# 2")
        reservation_display['list'].heading("# 2", text="Table Number")
        reservation_display['list'].column("# 3")
        reservation_display['list'].heading("# 3", text="Customer Name")
        reservation_display['list'].column("# 4")
        reservation_display['list'].heading("# 4", text="Time Booked")
        reservation_display['list'].column("# 5")
        reservation_display['list'].heading("# 5", text="Number of people")

        for reservation in current_user.get_restaurant().get_reservations():
            reservation_display['list'].insert('', 'end', text=str(reservation.get_reservation_ID()),
                                               values=(str(reservation.get_reservation_ID()),
                                                       str(reservation.get_table().get_table_number()),
                                                       reservation.get_customer_name(),
                                                       reservation.get_time(),
                                                       reservation.get_num_people()))

        y_scrollbar = ttk.Scrollbar(self, orient="vertical", command=reservation_display['list'].yview)
        reservation_display['list'].configure(yscrollcommand=y_scrollbar.set)
        y_scrollbar.pack(side="right", fill="y")

        # defining the buttons
        buttons['add'] = ttk.Button(reservation_frame, text="Add Reservation ", width=45,
                                    command=lambda: (
                                        self.open_new_window(ReservationsAdd, "Add Reservation", self.refresh)))

        buttons['update'] = ttk.Button(reservation_frame, text="Update Reservation", width=45,
                                       command=lambda: self.open_new_window(ReservationsUpdate, "Update Reservation",
                                                                            self.refresh, reservation_display['list']))

        buttons['delete'] = ttk.Button(reservation_frame, text="Delete Reservation", width=45,
                                       command=lambda: self.begin_delete_reservation(reservation_display['list']))

        index = 2
        # displaying the list box
        for display in reservation_display.values():
            display.pack(fill='both', expand=True, pady=10, padx=10)
            index += 1

        # displaying the buttons
        for button in buttons.values():
            button.pack(pady=5, padx=5)
            index += 1
        return reservation_frame

    # function refreshing the contents in the tree view
    def refresh(self):
        refresh_current_user()
        for widget in self.winfo_children():
            widget.destroy()
        reservation_view = self.create_widgets()
        reservation_view.pack()

    def open_new_window(self, root, title, callback, reservation=None):
        new_window = tk.Toplevel(self)
        new_window.title(title)
        print(reservation)
        if reservation is None:
            new_frame = root(new_window, callback)
            new_frame.pack()
            return True
        else:
            current_item = reservation.focus()
            reservation_details = reservation.item(current_item, 'values')
            new_frame = root(new_window, callback, reservation_details)
            new_frame.pack()
            return True

    def begin_delete_reservation(self, reservation):
        if reservation is None:
            tkm.showerror("Selection needed!", "You need to select a reservation first before you can delete it!")
            return False
        else:
            current_item = reservation.focus()
            reservation_details = reservation.item(current_item, 'values')
            if askyesno("Delete this reservation", "Are you sure you want to delete this reservation?"):
                delete_reservation(reservation_details)
                self.refresh()
