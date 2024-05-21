# Author: Lewis Quick , Student ID: 22016949
import tkinter as tk
from tkinter import ttk
from main import *

font = ("Arial", 14)


class AccountManagement(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        view = self.create_widgets()
        view.pack()

    def create_widgets(self):
        frame = ttk.Frame(self)
        oldPswd = tk.StringVar()
        newPswd = tk.StringVar()
        newPswd2 = tk.StringVar()
        chpDisplay = {}
        chpDisplay["title"] = ttk.Label(frame, text="Change Password", font=font)
        chpDisplay["oldPswdLabel"] = ttk.Label(frame, text="Old Password:", font=font)
        chpDisplay["oldPswdInput"] = ttk.Entry(frame, textvariable=oldPswd, show="*", font=font)
        chpDisplay["newPswdLabel"] = ttk.Label(frame, text="New Password:", font=font)
        chpDisplay["newPswdInput"] = ttk.Entry(frame, textvariable=newPswd, show="*", font=font)
        chpDisplay["newPswd2Label"] = ttk.Label(frame, text="Re-enter New Password:", font=font)
        chpDisplay["newPswd2Input"] = ttk.Entry(frame, textvariable=newPswd2, show="*", font=font)
        chpDisplay["submitButton"] = ttk.Button(frame, text="Submit",
                                                command=lambda: self.begin_password_change(oldPswd, newPswd, newPswd2))

        index = 3
        # displaying the widgets
        for display in chpDisplay.values():
            display.pack(fill='both', expand=True, pady=10, padx=10)
            index += 1
        return frame

    def begin_password_change(self, oldPswd, newPswd, newPswd2):
        if change_password(oldPswd, newPswd, newPswd2):
            tkm.showinfo("Logging out", "Since the password has been changed you will now be logged out")
            logout(self)
