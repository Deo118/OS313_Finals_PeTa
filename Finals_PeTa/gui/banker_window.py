# Banker's Algorithm Window (Single Resource Type)

import random
import customtkinter as ctk
from tkinter import messagebox

from backend.banker import Banker
from gui.utils import center_window, bring_to_front, animate_entry


def open_banker_window(parent):
    win = ctk.CTkToplevel(parent)
    win.title("Banker's Algorithm (1 Resource Type)")
    win.resizable(False, False)
    center_window(win, 900, 600)
    bring_to_front(win)

    ctk.CTkLabel(
        win,
        text="Banker's Algorithm Simulator (1 Resource Type)",
        font=ctk.CTkFont(size=16, weight="bold")
    ).pack(pady=10)

    controls = ctk.CTkFrame(win)
    controls.pack(padx=12, pady=6, fill="x")

    ctk.CTkLabel(controls, text="Number of Processes:").grid(row=0, column=0, padx=6)
    entry_np = ctk.CTkEntry(controls, width=80, justify="center")
    entry_np.grid(row=0, column=1, padx=6)

    ctk.CTkLabel(controls, text="(Single resource type only)").grid(row=0, column=2, padx=6)

    ctk.CTkButton(controls, text="Set Processes", width=120,
                  command=lambda: create_entries()).grid(row=0, column=3, padx=8)

    ctk.CTkButton(controls, text="Auto Generate", width=120,
                  command=lambda: auto_generate()).grid(row=0, column=4, padx=8)

    frame_scroll = ctk.CTkScrollableFrame(win, width=860, height=340)
    frame_scroll.pack(padx=10, pady=10, fill="both", expand=True)

    avail_frame = ctk.CTkFrame(win)
    avail_frame.pack(pady=6)
    ctk.CTkLabel(avail_frame, text="Available Resources:").grid(row=0, column=0, padx=6)

    entry_avail = ctk.CTkEntry(avail_frame, width=120, justify="center")
    entry_avail.grid(row=0, column=1, padx=6)
    entry_avail.insert(0, "3")

    entries = []  # list of tuples (current_entry, max_entry)
    
    # Create process entries
    def create_entries():
        nonlocal entries
        for w in frame_scroll.winfo_children():
            w.destroy()
        entries = []

        try:
            n = int(entry_np.get())
            if n <= 0:
                raise ValueError
        except Exception:
            messagebox.showerror("Error", "Enter valid number of processes.")
            return

        header = ctk.CTkFrame(frame_scroll)
        header.grid(row=0, column=0, pady=(0, 8))
        ctk.CTkLabel(header, text="Process").grid(row=0, column=0, padx=10)
        ctk.CTkLabel(header, text="Current Resources").grid(row=0, column=1, padx=40)
        ctk.CTkLabel(header, text="Maximum Resources").grid(row=0, column=2, padx=40)

        for i in range(n):
            row = ctk.CTkFrame(frame_scroll)
            row.grid(row=i + 1, column=0, pady=6, sticky="w")

            ctk.CTkLabel(row, text=f"P{i}").grid(row=0, column=0, padx=10)

            cur = ctk.CTkEntry(row, width=120, justify="center")
            cur.grid(row=0, column=1, padx=20)

            mx = ctk.CTkEntry(row, width=120, justify="center")
            mx.grid(row=0, column=2, padx=20)

            entries.append((cur, mx))
    
    # Auto-generate 
    def auto_generate():
        try:
            n = int(entry_np.get())
            if n <= 0:
                raise ValueError
        except Exception:
            messagebox.showerror("Error", "Enter number of processes first.")
            return

        if not entries or len(entries) != n:
            create_entries()

        available = random.randint(1, 6)
        entry_avail.delete(0, "end")
        entry_avail.insert(0, str(available))

        for i in range(n):
            cur_val = random.randint(0, available)
            mx_val = cur_val + random.randint(0, 6)
            animate_entry(entries[i][0], cur_val, min_val=0, max_val=available)
            animate_entry(entries[i][1], mx_val, min_val=cur_val, max_val=mx_val)
    # Run 
    def run_banker():
        try:
            n = int(entry_np.get())
            if n <= 0:
                raise ValueError
        except Exception:
            messagebox.showerror("Error", "Enter valid process count.")
            return

        allocation = []
        maximum = []

        try:
            for i in range(n):
                cur_text = entries[i][0].get().strip()
                max_text = entries[i][1].get().strip()

                cur = int(cur_text) if cur_text != "" else 0
                mx = int(max_text) if max_text != "" else 0

                allocation.append([cur])
                maximum.append([mx])

            avail = [int(entry_avail.get().strip())]
        except Exception as e:
            messagebox.showerror("Input error", str(e))
            return

        steps, safe, sequence = Banker.is_safe(allocation, maximum, avail)
        show_output(steps, safe, sequence, allocation, maximum, avail)

    # Output window
    def show_output(steps, safe, sequence, allocation, maximum, avail):
        win.withdraw()

        out = ctk.CTkToplevel()
        out.title("Banker's Algorithm - Results")
        center_window(out, 900, 520)
        bring_to_front(out)

        ctk.CTkLabel(
            out,
            text="Banker's Algorithm Output",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=8)

        txt = ctk.CTkTextbox(out, width=860, height=420, wrap="none")
        txt.pack(padx=10, pady=6, fill="both", expand=True)
        txt.configure(font=("Courier New", 12))

        w_proc = 12
        w_val = 22

        header_line = (
            f"{'Process':<{w_proc}}"
            f"{'Current Resources':^{w_val}}"
            f"{'Maximum Resources':^{w_val}}"
            f"{'Needed Resources':^{w_val}}"
            f"{'Available Resources':^{w_val}}\n"
        )

        sep = "-" * len(header_line.rstrip("\n")) + "\n"

        txt.insert("end", header_line)
        txt.insert("end", sep)

        initial_av = avail[0]

        for i in range(len(allocation)):
            cur = allocation[i][0]
            mx = maximum[i][0]
            need = mx - cur

            txt.insert(
                "end",
                f"{f'P{i}':<{w_proc}}"
                f"{str(cur):^{w_val}}"
                f"{str(mx):^{w_val}}"
                f"{str(need):^{w_val}}"
                f"{str(initial_av):^{w_val}}\n"
            )

        txt.insert("end", "\n")
        
        txt.insert("end", "\nStep-by-step checks:\n")

        for step_i, step in enumerate(steps, start=1):
            pid = step["process"]
            need = step["need"][0]
            avb = step["available_before"][0]
            comp = "≤" if need <= avb else "≥"
            txt.insert(
                "end",
                f"Step {step_i}: P{pid} - Needed Resources: [{need}] {comp} "
                f"Available Resources: [{avb}] -> Can run: {step['can_run']}\n"
            )

        txt.insert("end", "\n")

        if safe:
            seq = " -> ".join(f"P{i}" for i in sequence)
            txt.insert("end", f"System is in a SAFE STATE.\nSafe sequence: {seq}\n")
        else:
            txt.insert("end", "System is in an UNSAFE STATE. Deadlock possible.\n")

        txt.configure(state="disabled")

        def back():
            out.destroy()
            win.deiconify()

        ctk.CTkButton(out, text="Back to Input", command=back).pack(pady=8)

    ctk.CTkButton(win, text="Run Banker's Algorithm",
                  command=run_banker).pack(pady=8)

    win.mainloop()
