# Register Window
# Allows creation of new user accounts.

import customtkinter as ctk
from tkinter import messagebox

from backend.accounts import AccountManager
from gui.utils import center_window, bring_to_front

# Shared account manager
acct_mgr = AccountManager()

def open_register_window(parent=None):
    # Create window
    reg_win = ctk.CTkToplevel(parent)
    reg_win.title("Register Account")
    reg_win.resizable(False, False)
    center_window(reg_win, 360, 220)
    bring_to_front(reg_win)

    # Title
    ctk.CTkLabel(
        reg_win,
        text="Register New Account",
        font=ctk.CTkFont(size=16, weight="bold")
    ).pack(pady=10)

    # Frame
    frm = ctk.CTkFrame(reg_win)
    frm.pack(padx=12, pady=6, fill="both")

    # Username
    ctk.CTkLabel(frm, text="Username:").grid(row=0, column=0, sticky="w", padx=6, pady=6)
    user_entry = ctk.CTkEntry(frm, width=200)
    user_entry.grid(row=0, column=1, padx=6, pady=6)

    # Password
    ctk.CTkLabel(frm, text="Password:").grid(row=1, column=0, sticky="w", padx=6, pady=6)
    pw_entry = ctk.CTkEntry(frm, width=200, show="*")
    pw_entry.grid(row=1, column=1, padx=6, pady=6)

    # Registration logic
    def do_register():
        u = user_entry.get().strip()
        p = pw_entry.get().strip()
        if not u or not p:
            messagebox.showerror("Error", "Username and password required.")
            return

        ok, msg = acct_mgr.register(u, p)
        if ok:
            messagebox.showinfo("Success", msg)
            reg_win.destroy()
        else:
            messagebox.showerror("Error", msg)

    # Submit
    ctk.CTkButton(reg_win, text="Register", command=do_register).pack(pady=10)

    return reg_win
