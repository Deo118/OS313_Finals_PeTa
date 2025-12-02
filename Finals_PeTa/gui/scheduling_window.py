# CPU Scheduling Window
# Handles inputs, auto-generate animation, running algorithms, and displaying Gantt chart + results.

import random
import customtkinter as ctk
from tkinter import messagebox

from backend.scheduling import CPUScheduler, Process
from gui.utils import center_window, bring_to_front, animate_entry


def open_scheduling_window(parent):
    # Window setup
    win = ctk.CTkToplevel(parent)
    win.title("CPU Scheduling Simulator")
    win.resizable(False, False)
    center_window(win, 760, 700)
    bring_to_front(win)

    entries = []
    algo_choice = ctk.StringVar(value="FCFS (First-Come-First-Serve)")

    # Left panel
    left_frame = ctk.CTkFrame(win)
    left_frame.pack(fill="both", padx=20, pady=20, expand=True, side="left")

    # Controls
    controls = ctk.CTkFrame(left_frame)
    controls.pack(pady=10, anchor="center")

    # Algorithm dropdown
    ctk.CTkLabel(controls, text="Choose Algorithm:").grid(row=0, column=0, pady=(0, 8))
    algo_menu = ctk.CTkOptionMenu(
        controls,
        values=[
            "FCFS (First-Come-First-Serve)",
            "SJF (Non-Preemptive)",
            "SJF (Preemptive)",
            "Priority (Non-Preemptive)",
            "Priority (Preemptive)",
            "Round Robin"
        ],
        variable=algo_choice,
        command=lambda v: refresh_entries(),
        width=220
    )
    algo_menu.grid(row=1, column=0, pady=(0, 10))

    # Auto-generate
    ctk.CTkButton(controls, text="Auto Generate", command=lambda: auto_generate()).grid(row=2, column=0, pady=6)

    # Number of processes
    ctk.CTkLabel(controls, text="Number of Processes:").grid(row=0, column=1, pady=(0, 8))
    entry_n = ctk.CTkEntry(controls, width=120, justify="center")
    entry_n.grid(row=1, column=1)

    ctk.CTkButton(controls, text="Set Processes", command=lambda: create_entries()).grid(row=2, column=1, pady=6)

    # Quantum (for Round Robin only)
    quantum_frame = ctk.CTkFrame(controls, fg_color="transparent")
    ctk.CTkLabel(quantum_frame, text="Quantum (RR):").pack()
    entry_q = ctk.CTkEntry(quantum_frame, width=120, justify="center")
    entry_q.pack()
    quantum_frame.grid(row=0, column=2, rowspan=3, padx=10)
    quantum_frame.grid_remove()

    frame_inputs = ctk.CTkScrollableFrame(left_frame, width=700, height=340)
    frame_inputs.pack(pady=10, padx=10, fill="both", expand=True)

    # Create dynamic process entries
    def create_entries():
        nonlocal entries
        for w in frame_inputs.winfo_children():
            w.destroy()
        entries = []

        try:
            n = int(entry_n.get())
            if n <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Enter valid number of processes.")
            return

        is_priority = "Priority" in algo_choice.get()

        for i in range(n):
            ctk.CTkLabel(frame_inputs, text=f"P{i+1} Arrival Time:").grid(row=i, column=0, padx=5, pady=4)
            at = ctk.CTkEntry(frame_inputs, width=80, justify="center")
            at.grid(row=i, column=1, padx=5)

            ctk.CTkLabel(frame_inputs, text="Burst Time:").grid(row=i, column=2)
            bt = ctk.CTkEntry(frame_inputs, width=80, justify="center")
            bt.grid(row=i, column=3, padx=5)

            if is_priority:
                ctk.CTkLabel(frame_inputs, text="Priority:").grid(row=i, column=4)
                pr = ctk.CTkEntry(frame_inputs, width=80, justify="center")
                pr.grid(row=i, column=5, padx=5)
            else:
                pr = ctk.CTkEntry(frame_inputs, width=80, justify="center")

            entries.append((at, bt, pr))

    # Refresh when algorithm type changes
    def refresh_entries():
        if algo_choice.get().startswith("Round Robin"):
            quantum_frame.grid()
        else:
            quantum_frame.grid_remove()
        create_entries()
    
    # Auto generate sample data
    def auto_generate():
        try:
            n = int(entry_n.get())
        except:
            messagebox.showerror("Error", "Set process count first.")
            return

        if not entries or len(entries) != n:
            create_entries()

        is_priority = "Priority" in algo_choice.get()

        for i in range(n):
            at = random.randint(0, 10)
            bt = random.randint(1, 12)
            animate_entry(entries[i][0], at)
            animate_entry(entries[i][1], bt)

            if is_priority:
                pr = random.randint(1, 5)
                animate_entry(entries[i][2], pr)
            else:
                entries[i][2].delete(0, "end")
  
    # Simulation executor
    def run_sim():
        try:
            n = int(entry_n.get())
        except:
            messagebox.showerror("Error", "Enter valid number of processes.")
            return

        procs = []
        for i in range(n):
            try:
                at = int(entries[i][0].get())
                bt = int(entries[i][1].get())
                pr = int(entries[i][2].get()) if "Priority" in algo_choice.get() else 0
            except:
                messagebox.showerror("Error", f"Invalid data in P{i+1}")
                return
            procs.append(Process(f"P{i+1}", at, bt, pr))

        algorithm = algo_choice.get()

        try:
            if algorithm.startswith("FCFS"):
                result = CPUScheduler.fcfs(procs)

            elif algorithm.startswith("SJF") and "Non" in algorithm:
                result = CPUScheduler.sjf(procs)

            elif algorithm.startswith("SJF") and "Preemptive" in algorithm:
                result = CPUScheduler.sjf_preemptive(procs)

            elif algorithm.startswith("Priority") and "Non" in algorithm:
                result = CPUScheduler.priority(procs)

            elif algorithm.startswith("Priority") and "Preemptive" in algorithm:
                result = CPUScheduler.priority_preemptive(procs)

            elif algorithm.startswith("Round Robin"):
                q = int(entry_q.get())
                result = CPUScheduler.round_robin(procs, q)

        except Exception as e:
            messagebox.showerror("Algorithm Error", str(e))
            return

        show_output(result)
   
    # Display result window
    def show_output(result):
        win.withdraw()
        out = ctk.CTkToplevel()
        out.title("CPU Scheduling - Results")
        center_window(out, 800, 600)
        bring_to_front(out)

        ctk.CTkLabel(out, text="OUTPUT", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        txt = ctk.CTkTextbox(out, width=760, height=460, wrap="none")
        txt.pack(fill="both", expand=True, padx=10, pady=10)
        txt.configure(font=("Courier New", 12))

        timeline = result["timeline"]
        table = result["table"]

        # Gantt chart
        txt.insert("end", "Gantt Chart:\n\n")
        segments = [f"| {seg['pid']} " for seg in timeline]
        widths = [len(seg) for seg in segments]

        txt.insert("end", "Process Timeline:  ")
        for s in segments:
            txt.insert("end", s)
        txt.insert("end", "|\n")

        txt.insert("end", "Finish Times:     ")
        for seg, w in zip(timeline, widths):
            txt.insert("end", str(seg["start"]).ljust(w))
        if timeline:
            txt.insert("end", str(timeline[-1]["finish"]) + "\n\n")

        # Table header
        txt.insert("end", f"{'Process':<10}{'AT':<10}{'BT':<10}{'WT':<10}{'TAT':<10}\n")
        txt.insert("end", "-" * 50 + "\n")

        for row in table:
            txt.insert("end",
                f"{row['pid']:<10}{row['arrival']:<10}{row['burst']:<10}{row['wait']:<10}{row['tat']:<10}\n"
            )

        txt.insert("end", f"\nAverage Waiting Time = {result['avg_wt']:.2f}\n")
        txt.insert("end", f"Average Turnaround Time = {result['avg_tat']:.2f}\n")

        txt.configure(state="disabled")

        # Back button
        def back():
            out.destroy()
            win.deiconify()

        ctk.CTkButton(out, text="Back to Input", command=back).pack(pady=12)

    # Run button
    ctk.CTkButton(left_frame, text="Run Simulation", command=run_sim).pack(pady=10)

    win.mainloop()
