# Login Window
# Uses AccountManager and redirects to main menu.

import customtkinter as ctk
from tkinter import messagebox

from backend.accounts import AccountManager
from gui.utils import center_window, bring_to_front
from gui.register_window import open_register_window

# Global account manager instance
acct_mgr = AccountManager()


def open_login_window():
    # Create main login window
    login_win = ctk.CTk()
    login_win.title("OS Simulator - Login")
    login_win.resizable(False, False)
    center_window(login_win, 380, 300)
    bring_to_front(login_win)

    # Title
    ctk.CTkLabel(
        login_win,
        text="OS Simulator Login",
        font=ctk.CTkFont(size=18, weight="bold")
    ).pack(pady=12)

    # Frame for inputs
    frm = ctk.CTkFrame(login_win)
    frm.pack(padx=12, pady=6, fill="both")

    # Username
    ctk.CTkLabel(frm, text="Username:").grid(row=0, column=0, sticky="w", padx=6, pady=8)
    user_entry = ctk.CTkEntry(frm, width=200)
    user_entry.grid(row=0, column=1, padx=6, pady=8)

    # Password
    ctk.CTkLabel(frm, text="Password:").grid(row=1, column=0, sticky="w", padx=6, pady=8)
    pw_entry = ctk.CTkEntry(frm, width=200, show="*")
    pw_entry.grid(row=1, column=1, padx=6, pady=8)

    # Login logic
    def do_login(event=None):
        from gui.main_menu import open_main_menu
        u = user_entry.get().strip()
        p = pw_entry.get().strip()
        ok, msg = acct_mgr.login(u, p)

        if ok:
            messagebox.showinfo("Welcome", msg)
            login_win.destroy()
            open_main_menu(u)
        else:
            messagebox.showerror("Login Failed", msg)

    # Buttons
    ctk.CTkButton(
        login_win, text="Login", width=140, command=do_login
    ).pack(pady=8)

    ctk.CTkButton(
        login_win, text="Register", width=140,
        command=lambda: open_register_window(login_win)
    ).pack()

    # Enter key triggers login
    login_win.bind("<Return>", do_login)

    login_win.mainloop()
