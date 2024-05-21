# Author: Zahin Hussain, Student ID: 22016373 and  Beyzanur Kayaci Student ID:22066921
from tkinter import ttk
import tkinter as tk
from tkinter import LEFT, W
from main import *
from orderManager import OrderViewer
from reservationViewer import ReservationViewer
from inventoryViewer import InventoryViewer
from menuViewer import MenuManagement
from accountManager import AccountManagement
from tableViewer import TableViewer
from tkcalendar import Calendar

font = ("Arial", 14)


class App(tk.Tk):
    initialize_objects(load=0)

    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Horizon Restaurants Main Menu:')
        self.geometry('1366x768')
        self.resizable(0, 0)
        self.configure(background="#252526")

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=10)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=10)

        self.__create_main_window()

        self.frames = {}

        for F in (
                AccountManagement, ReservationViewer, InventoryViewer,
                MenuManagement, Discounts,
                Report, User, OrderViewer, TableViewer, Pay):
            frame = F(self)

            self.frames[F] = frame

    def __create_main_window(self):
        side_menu = SideMenu(self)
        side_menu.grid(column=0, row=1, rowspan=10, sticky="nsw")
        # nav menu
        menu_bar = MenuBar(self)
        self.config(menu=menu_bar)

    def show_frame(self, cont):
        print("Working")
        frame = self.frames[cont]
        frame.tkraise()
        frame.grid(column=1, row=1, columnspan=10, rowspan=10, sticky="nesw", padx=10, pady=10, ipadx=10,
                   ipady=10)


class Housing(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.configure(bg="white")


class SideMenu(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.configure(highlightbackground="blue", highlightthickness=2)
        self.configure(bg="#0A0A0A")

        self.reservation_management = tk.Button(self, text="Reservation Manager", width=35, height=2, pady=5, padx=0,
                                                command=lambda: app.show_frame(ReservationViewer))
        self.order_management = tk.Button(self, text="Order Management", width=35, height=2, pady=5, padx=0,
                                          command=lambda: app.show_frame(OrderViewer))

        self.pay = tk.Button(self, text="Pay", width=35, height=2, pady=5, padx=0,
                             command=lambda: app.show_frame(Pay))
        # kitchen staff

        self.anchor = LEFT
        self.order_management.configure(bg='#0A0A0A', fg='white')
        self.reservation_management.configure(bg='#0A0A0A', fg='white')
        self.pay.configure(bg='#0A0A0A', fg='white')
        self.order_management.grid(row=6, sticky="w", ipady=5)
        self.reservation_management.grid(row=7, sticky="w", ipady=5)
        self.pay.grid(row=9, sticky="w", ipady=5)
        self.anchor = W


class MenuBar(tk.Menu):
    def __init__(self, container):
        super().__init__(container)

        # add commands to the menu
        self.add_command(label='HOME', command=self.on_home)
        self.add_command(label='ACCOUNT', command=self.on_account)
        self.add_command(label='BACK', command=self.on_back)
        self.add_command(label='EXIT', command=self.on_exit)

    def on_home(self):
        print("Home button clicked")

    def on_account(self):
        print("Account button clicked")

    def on_back(self):
        print("Back button clicked")

    def on_exit(self):
        print("Exit button clicked")
        self.quit()

    # frames for indivial pages


class Pay(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Placement for order receipts and payment
        label_order = tk.Label(self, text="Enter Order Number", font=10)
        label_order.grid(row=0, column=0, padx=10, pady=10)

        order_entry = tk.Entry(self, width=30)
        order_entry.grid(row=1, column=0, pady=5)

        payment_button = tk.Button(self, text="Payment", width=35, height=2)
        payment_button.grid(row=2, column=0, pady=5)

        # Placement for order recipes
        label_recipes = tk.Label(self, text="Enter Order Number", font=10)
        label_recipes.grid(row=0, column=1, padx=10, pady=10)

        order_recipes = tk.Entry(self, width=30)
        order_recipes.grid(row=1, column=1, columnspan=2, pady=5)

        recipes_button = tk.Button(self, text="Recipes", width=35, height=2)
        recipes_button.grid(row=2, column=1)


# each frame
class Discounts(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # label of frame Layout 2
        label = tk.Label(self, text="Startpage", font=10)
        label.grid(row=0, column=4, padx=10, pady=10)


class Report(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.configure(bg="#f2f2f2")  # Set background color

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Use a modern font
        modern_font = ("Arial", 12)

        self.sales = tk.Button(self, text="Sales", width=35)
        self.serving_time = tk.Button(self, text="Serving time", width=35)
        self.bookings = tk.Button(self, text="Bookings", width=35)
        self.inventory_rep = tk.Button(self, text="Inventory", width=35)

        # Date beginning
        tk.Label(self, text='Date beginning:', font=modern_font, background="#f2f2f2").grid(row=2, column=0,
                                                                                            sticky=tk.E, padx=10,
                                                                                            pady=5)
        self.cal_beginning = Calendar(self, selectmode="day", year=2023, month=1, day=1, background="#ffffff",
                                      foreground="#333333")
        self.cal_beginning.grid(row=3, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)

        # Date ending
        tk.Label(self, text='Date ending:', font=modern_font, background="#f2f2f2").grid(row=2, column=2, sticky=tk.E,
                                                                                         padx=10, pady=5)
        self.cal_ending = Calendar(self, selectmode="day", year=2023, month=1, day=1, background="#ffffff",
                                   foreground="#333333")
        self.cal_ending.grid(row=3, column=2, columnspan=2, sticky=tk.W, padx=10, pady=5)

        self.sales.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.serving_time.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.bookings.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.inventory_rep.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")


class User(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # label of frame Layout 2
        label = tk.Label(self, text="Startpage", font=10)
        label.grid(row=0, column=4, padx=10, pady=10)


class orderManagement(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # label of frame Layout 2
        label = tk.Label(self, text="Startpage", font=10)
        label.grid(row=0, column=4, padx=10, pady=10)


if __name__ == '__main__':
    app = App()
    # deleting file storing user info so user has to log in again when window closed
    app.protocol("WM_DELETE_WINDOW", lambda: close_window(app))
    app.mainloop()
