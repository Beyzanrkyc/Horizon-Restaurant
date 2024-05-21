# Author: William Forber, Student ID: 22015706
import tkinter as ttk
import tkinter as tk
from tkcalendar import Calendar
from tktimepicker import SpinTimePickerModern
from tktimepicker import constants
from main import *
from datetime import datetime

# loading the current user
initialize_objects(1)


def check_capacity(table, num_people):
    if table.get_capacity() >= num_people:
        return True
    else:
        return False


def get_available_tables(number_people, cal, time):
    refresh_current_user()
    current_user = load_current_user()
    num_people = number_people.get()
    if not num_people:
        return False
    else:
        num_people = int(num_people)

    tables_to_list = []

    booking_datetime = get_booking_datetime(cal, time)  # assuming you have a method to get the booking datetime

    for table in current_user.get_restaurant().get_tables():
        if check_capacity(table, num_people):
            reservations_for_table = [reservation for reservation in
                                      current_user.get_restaurant().get_reservations() if
                                      reservation.get_table() == table]

            if all(is_table_available(booking_datetime, reservation.get_time()) for reservation in
                   reservations_for_table):
                tables_to_list.append(table)

    return tables_to_list


def is_table_available(booking_datetime, reservation_time):
    if reservation_time is None:
        return True

    # Check if the table is more than three hours away from the booking time
    min_booking_time = booking_datetime - timedelta(hours=3)
    max_booking_time = booking_datetime + timedelta(hours=3)

    return reservation_time < min_booking_time or reservation_time > max_booking_time


def get_booking_datetime(cal, time):
    date_str = cal.get_date()
    time_str = time.hours()
    dateandtime = str(date_str) + ' ' + str(time_str) + ':00:00'
    booking_datetime = datetime.strptime(dateandtime, '%m/%d/%y %H:%M:%S')
    return booking_datetime


def update_available_tables(available_tables_selection, num_people, cal, time):
    tables_to_list = get_available_tables(num_people, cal, time)
    if not tables_to_list:
        return False
    available_tables_selection.delete(0, tk.END)
    for table in tables_to_list:
        available_tables_selection.insert(tk.END, "Table " + str(table.get_table_number()))


class ReservationsAdd(tk.Frame):

    def __init__(self, container, callback):
        super().__init__(container)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.callback = callback
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Title
        self.title = ttk.Label(self, text='Reservation Form', font=('Helvetica', 16))
        self.title.grid(row=0, column=0, columnspan=3, pady=10)

        # Reservation name
        ttk.Label(self, text='Name:').grid(row=1, column=0, sticky=tk.E, padx=10)
        self.name_entry = ttk.Entry(self, width=30)
        self.name_entry.focus()
        self.name_entry.grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=5)

        # Reservation date
        ttk.Label(self, text='Date:').grid(row=2, column=0, sticky=tk.E, padx=10)
        self.cal = Calendar(self, selectmode="day", year=datetime.now().year, month=datetime.now().month,
                            day=datetime.now().day)
        self.cal.config(mindate=datetime.now())
        self.cal.grid(row=2, column=1, columnspan=2, sticky=tk.W, pady=5)
        # Time add
        ttk.Label(self, text='Time:').grid(row=3, column=0, sticky=tk.E, padx=10)
        self.time_picker = SpinTimePickerModern(self)
        self.time_picker.addAll(constants.HOURS24)  # adds hours clock, minutes and period
        self.time_picker.configureAll(bg="#404040", height=1, fg="#ffffff", font=("Times", 16), hoverbg="#404040",
                                      hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")
        self.time_picker.configure_separator(bg="#404040", fg="#ffffff")
        self.time_picker.setMins(0)
        self.time_picker.set24Hrs(12)
        self.time_picker.grid(row=3, column=1, columnspan=2, sticky=tk.W, pady=5)

        # Number of people
        ttk.Label(self, text='Number of people:').grid(row=4, column=0, sticky=tk.E, padx=10)
        self.number_people = ttk.Entry(self, width=30)
        self.number_people.focus()
        self.number_people.grid(row=4, column=1, columnspan=2, sticky=tk.W, pady=5)

        ttk.Label(self, text='Available Tables:').grid(row=5, column=0, sticky=tk.E, padx=10)
        self.available_tables_selection = ttk.Listbox(self, selectmode="single")
        self.available_tables_selection.grid(row=5, column=1, sticky=tk.E, padx=10)
        # Button

        self.button = ttk.Button(self, text="Add Reservation", width=35, pady=5, padx=5,
                                 command=lambda: self.begin_add_reservation())
        self.button.grid(row=6, column=0, columnspan=2, pady=10)
        self.cal.bind("<<CalenderSelected>>",
                      lambda event: update_available_tables(self.available_tables_selection,
                                                            self.number_people, self.cal, self.time_picker))
        self.cal.bind("<Enter>",
                      lambda event: update_available_tables(self.available_tables_selection,
                                                            self.number_people, self.cal, self.time_picker))
        self.cal.bind("<Leave>",
                      lambda event: update_available_tables(self.available_tables_selection,
                                                            self.number_people, self.cal, self.time_picker))
        self.time_picker.bind("<<TimePickerChanged>>",
                              lambda event: update_available_tables(self.available_tables_selection,
                                                                    self.number_people, self.cal, self.time_picker))
        self.time_picker.bind("<Enter>", lambda event: update_available_tables(self.available_tables_selection,
                                                                               self.number_people, self.cal,
                                                                               self.time_picker))
        self.time_picker.bind("<Leave>", lambda event: update_available_tables(self.available_tables_selection,
                                                                               self.number_people, self.cal,
                                                                               self.time_picker))
        self.number_people.bind("<FocusOut>", lambda event: update_available_tables(self.available_tables_selection,
                                                                                    self.number_people, self.cal,
                                                                                    self.time_picker))
        self.number_people.bind("<Leave>", lambda event: update_available_tables(self.available_tables_selection,
                                                                                 self.number_people, self.cal,
                                                                                 self.time_picker))

    def begin_add_reservation(self):
        date = self.cal.get_date()
        time = self.time_picker.hours()
        customer_name = self.name_entry.get()
        num_people = self.number_people.get()
        if not num_people:
            tkm.showerror("Error creating reservation!", "All fields need to be inputted to add a reservation!")
            return False
        else:
            num_people = int(num_people)
        if not customer_name or not self.number_people.get():
            tkm.showerror("Error creating reservation!", "All fields need to be inputted to add a reservation!")
            return False
        add_reservation(date, time, customer_name, num_people, self.available_tables_selection)
        self.callback()
        self.master.destroy()


class ReservationsUpdate(ReservationsAdd):
    def __init__(self, container, callback, reservation_details):
        super().__init__(container, callback)
        self.res_id = reservation_details[0]
        self.table_number = reservation_details[1]
        self.customer_name = reservation_details[2]
        self.date_and_time = reservation_details[3]
        self.date_and_time = datetime.strptime(self.date_and_time, '%Y-%m-%d %H:%M:%S')
        date = self.date_and_time.date()
        time = self.date_and_time.time()
        time = time.hour
        num_people = reservation_details[4]
        self.name_entry.insert(0, self.customer_name)
        self.cal.selection_set(date)
        self.time_picker.set24Hrs(time)
        self.number_people.insert(0, num_people)
        self.button.grid_forget()
        self.button = ttk.Button(self, text="Update Reservation", width=35, pady=5, padx=5,
                                 command=lambda: self.begin_update_reservation())
        self.button.grid(row=6, column=0, columnspan=2, pady=10)

    def begin_update_reservation(self):
        if not (self.name_entry.get() or self.number_people.get()):
            tkm.showerror("Error updating reservation!",
                          "The customers name and the number of people need to be inputted!")
            return False
        table_num = ""
        table = self.available_tables_selection
        for i in table.curselection():
            table = table.get(i)
        if not (isinstance(table, str)):
            table_num = self.table_number
        else:
            table_search = re.findall("[0-9]", table)
            for i in range(len(table_search)):
                table_num += str(table_search[i])
            table_num = int(table_num)
        update_reservation(self.name_entry.get(), self.cal.get_date(), self.time_picker.hours(),
                           self.number_people.get(), table_num, self.res_id)
        self.callback()
        self.master.destroy()


class ReservationRemove(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Title
        ttk.Label(self, text='Reservation Update', font=('Helvetica', 16), background='#f0f0f0').grid(row=0,
                                                                                                      column=0,
                                                                                                      columnspan=3,
                                                                                                      pady=10)

        # Reservation ID
        ttk.Label(self, text='Reservation ID:').grid(row=1, column=0, sticky=tk.E, padx=10)
        reservation_id_entry = ttk.Entry(self, width=30)
        reservation_id_entry.grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=5)

        # Reservation name
        ttk.Label(self, text='Name:').grid(row=2, column=0, sticky=tk.E, padx=10)
        name_entry = ttk.Entry(self, width=30)
        name_entry.grid(row=2, column=1, columnspan=2, sticky=tk.W, pady=5)

        # Reservation Phone number
        ttk.Label(self, text='Phone:').grid(row=3, column=0, sticky=tk.E, padx=10)
        phone_entry = ttk.Entry(self, width=30)
        phone_entry.grid(row=3, column=1, columnspan=2, sticky=tk.W, pady=5)

        # Button
        ttk.Button(self, text="Remove Reservation", width=35, height=2).grid(row=4, column=0, columnspan=3, pady=10)
