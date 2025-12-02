# Entry point for OS Simulator

import customtkinter as ctk
from gui.login_window import open_login_window


def main():
    # Theme initialization
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    # Launch login screen
    open_login_window()


if __name__ == "__main__":
    main()
