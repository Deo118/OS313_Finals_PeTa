# Main Menu Window
# Redirects to CPU Scheduling, Banker, and Page Replacement windows.

import customtkinter as ctk

from gui.utils import center_window, bring_to_front
from gui.scheduling_window import open_scheduling_window
from gui.banker_window import open_banker_window
from gui.paging_window import open_page_replacement_window

def logout(win):
    from gui.login_window import open_login_window
    win.destroy()
    open_login_window()


def open_main_menu(username):
    # Create main menu window
    menu = ctk.CTk()
    menu.title("OS Simulator - Main Menu")
    center_window(menu, 520, 360)
    menu.resizable(False, False)
    bring_to_front(menu)

    # Welcome text
    ctk.CTkLabel(
        menu,
        text=f"Welcome, {username}!",
        font=ctk.CTkFont(size=16, weight="bold")
    ).pack(pady=16)

    ctk.CTkLabel(menu, text="Choose a module:", font=ctk.CTkFont(size=12)).pack()

    # Button container
    btn_frame = ctk.CTkFrame(menu)
    btn_frame.pack(pady=18)

    # Modules
    ctk.CTkButton(
        btn_frame, text="CPU Scheduling", width=220,
        command=lambda: open_scheduling_window(menu)
    ).grid(row=0, column=0, pady=8)

    ctk.CTkButton(
        btn_frame, text="Banker's Algorithm", width=220,
        command=lambda: open_banker_window(menu)
    ).grid(row=1, column=0, pady=8)

    ctk.CTkButton(
        btn_frame, text="Page Replacement", width=220,
        command=lambda: open_page_replacement_window(menu)
    ).grid(row=2, column=0, pady=8)

    # Logout
    ctk.CTkButton(
        btn_frame, text="Logout", width=120,
        command=lambda: logout(menu)
    ).grid(row=3, column=0, pady=12)

    menu.mainloop()
