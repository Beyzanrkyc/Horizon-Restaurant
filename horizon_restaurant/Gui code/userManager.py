# Author: Lewis Quick , Student ID: 22016949
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from main import *

font = ("Arial", 14)


class ChngUser(tk.Frame):
    def __init__(self, container, callback, user):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.callback = callback
        self.user = user
        view = self.create_widgets()
        view.pack()

    def create_widgets(self):
        frame = ttk.Frame(self)
        user = None

        user0 = ''.join(self.user)
        for i in user_list:
            if i.get_user_name() == user0:
                user = i

        input = tk.StringVar()
        display = {}
        display["user"] = ttk.Label(frame, text="Enter Username:", font=font)
        display["userinput"] = ttk.Entry(frame, textvariable=input, font=font)
        display["submitButton"] = ttk.Button(frame, text="Submit", command=lambda: self.begin_user_set(user, input))

        for i in display.values():
            i.pack(fill='both', expand=True, pady=10, padx=10)

        return frame
    
    def begin_set_user(self, user, input):
        if input is not None:
            input = input.get()
            set_username(input, user)
        else:
            print("Enter username first")
        self.callback()
        self.master.destroy()

class ChngPswd(tk.Frame):
    def __init__(self, container, callback, user):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.callback = callback
        self.user = user
        view = self.create_widgets()
        view.pack()

    def create_widgets(self):
        frame = ttk.Frame(self)
        user = None

        user0 = ''.join(self.user)
        for i in user_list:
            if i.get_user_name() == user0:
                user = i

        input = tk.StringVar()
        display = {}
        display["pswd"] = ttk.Label(frame, text="Enter Password:", font=font)
        display["pswdInput"] = ttk.Entry(frame, textvariable=input, font=font)
        display["submitButton"] = ttk.Button(frame, text="Submit", command=lambda: self.begin_user_set(user, input))

        for i in display.values():
            i.pack(fill='both', expand=True, pady=10, padx=10)

        return frame
    
    def begin_set_pswd(self, user, input):
        if input is not None:
            input = input.get()
            set_password(input, user)
        else:
            print("Enter password first")
        self.callback()
        self.master.destroy()

class ChngPriv(tk.Frame):
    def __init__(self, container, callback, user):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.callback = callback
        self.user = user
        view = self.create_widgets()
        view.pack()

    def create_widgets(self):
        frame = ttk.Frame(self)
        user = None
        

        user0 = ''.join(self.user)
        for i in user_list:
            if i.get_user_name() == user0:
                user = i

        options = ["0", "1", "2"]
        input = tk.StringVar()
        display = {}
        display["priv"] = ttk.Label(frame, text="Enter Privilege:", font=font)
        display["privInput"] = ttk.OptionMenu(frame, input, *options)
        display["submitButton"] = ttk.Button(frame, text="Submit", command=lambda: self.begin_priv_set(user, input))

        for i in display.values():
            i.pack(fill='both', expand=True, pady=10, padx=10)

        return frame
    
    def begin_priv_set(self, user, input):
        if input is not None:
            input = input.get()
            set_privilege(input, user)
        else:
            print("Enter privilege first")
        self.callback()
        self.master.destroy()


class ChngRest(tk.Frame):
    def __init__(self, container, callback, user):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.callback = callback
        self.user = user
        view = self.create_widgets()
        view.pack()

    def create_widgets(self):
        frame = ttk.Frame(self)
        user = None

        user0 = ''.join(self.user)
        for i in user_list:
            if i.get_user_name() == user0:
                user = i

        options = []

        for i in restaurant_list:
            name = i.get_restaurant_name()
            options.append(name)
            
        input = tk.StringVar()
        display = {}
        display["rest"] = ttk.Label(frame, text="Enter Restaurant:", font=font)
        display["restInput"] = ttk.OptionMenu(frame, input, *options)
        display["submitButton"] = ttk.Button(frame, text="Submit", command=lambda: self.begin_rest_set(user, input))

        for i in display.values():
            i.pack(fill='both', expand=True, pady=10, padx=10)

        return frame
    
    def begin_rest_set(self, user, input):
        if input is not None:
            input = input.get()
            set_restaurant(input, user)
        else:
            print("Enter restaurant first")
        self.callback()
        self.master.destroy()



class AddUser(tk.Frame):
    def __init__(self, container, callback):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.callback = callback
        view = self.create_widgets()
        view.pack()

    def create_widgets(self):
        frame = ttk.Frame(self)
        username = tk.StringVar()
        password = tk.StringVar()
        privilege = tk.StringVar()
        restaurant = tk.StringVar()

        priv_options = ["0", "1", "2"]

        rest_options = []

        for i in restaurant_list:
            name = i.get_restaurant_name()
            rest_options.append(name)

        display = {}
        display["user"] = ttk.Label(frame, text="Enter Username:", font=font)
        display["userinput"] = ttk.Entry(frame, textvariable=username, font=font)
        display["pswd"] = ttk.Label(frame, text="Enter Password:", font=font)
        display["pswdInput"] = ttk.Entry(frame, textvariable=password, font=font)
        display["priv"] = ttk.Label(frame, text="Enter Privilege:", font=font)
        display["privInput"] = ttk.OptionMenu(frame, privilege, *priv_options)
        display["rest"] = ttk.Label(frame, text="Enter Restaurant:", font=font)
        display["restInput"] = ttk.OptionMenu(frame, restaurant, *rest_options)
        display["submitButton"] = ttk.Button(frame, text="Submit", command=lambda: self.begin_add_user(username,
                                                                            password, privilege, restaurant))

        for i in display.values():
            i.pack(fill='both', expand=True, pady=10, padx=10)

        return frame
    
    def begin_add_user(self, user, pswd, priv, rest):
        if user and pswd and priv and rest is not None:
            user = user.get()
            pswd = pswd.get()
            priv = priv.get()
            rest = rest.get()
            create_user(user, pswd, priv, rest)
        else:
            print("Missing parameters")
        self.callback()
        self.master.destroy()

