# Page Replacement Window

import random
import customtkinter as ctk
from tkinter import messagebox

from backend.paging import PageReplacement
from gui.utils import center_window, bring_to_front, animate_entry

def open_page_replacement_window(parent):
    win = ctk.CTkToplevel(parent)
    win.title("Page Replacement Simulator")
    win.resizable(False, False)
    center_window(win, 980, 620)
    bring_to_front(win)

    ctk.CTkLabel(
        win, text="Page Replacement Simulator",
        font=ctk.CTkFont(size=16, weight="bold")
    ).pack(pady=10)

    controls = ctk.CTkFrame(win)
    controls.pack(padx=12, pady=6, fill="x")

    # Reference string input
    ctk.CTkLabel(controls, text="Reference String (space-separated):").grid(
        row=0, column=0, padx=6, pady=6, sticky="w"
    )
    entry_refs = ctk.CTkEntry(controls, width=480)
    entry_refs.grid(row=0, column=1, padx=6, pady=6, sticky="w")

    # Frames input
    ctk.CTkLabel(controls, text="Number of Frames:").grid(
        row=1, column=0, padx=6, pady=6, sticky="w"
    )
    entry_frames = ctk.CTkEntry(controls, width=120, justify="center")
    entry_frames.grid(row=1, column=1, padx=6, pady=6, sticky="w")
    entry_frames.insert(0, "3")

    # Algorithm
    ctk.CTkLabel(controls, text="Algorithm:").grid(
        row=2, column=0, padx=6, pady=6, sticky="w"
    )
    algo_var = ctk.StringVar(value="FIFO")
    algo_menu = ctk.CTkOptionMenu(
        controls, values=["FIFO", "LRU", "Optimal"],
        variable=algo_var, width=140
    )
    algo_menu.grid(row=2, column=1, padx=6, pady=6, sticky="w")

    # Buttons
    ctk.CTkButton(
        controls, text="Auto Generate",
        width=140, command=lambda: auto_generate()
    ).grid(row=0, column=2, padx=8)

    ctk.CTkButton(
        controls, text="Run", width=120,
        command=lambda: run()
    ).grid(row=1, column=2, padx=8)

    # Helpers
    def parse_refs(text):
        parts = [p.strip() for p in text.split() if p.strip() != ""]
        return [int(x) for x in parts]

    # auto generate
    def auto_generate():
        length = random.randint(8, 18)
        max_page = random.randint(3, 9)

        refs = [random.randint(0, max_page) for _ in range(length)]
        refs_str = " ".join(str(x) for x in refs)

        nframes = random.randint(2, min(6, max_page + 1))

        from gui.utils import animate_text, animate_entry

        animate_text(entry_refs, refs_str, steps=10)
        animate_entry(entry_frames, nframes, min_val=1, max_val=10)

    # Output window
    def show_output(res):
        win.withdraw()

        out = ctk.CTkToplevel()
        out.title(f"Page Replacement - {res['algorithm']}")
        center_window(out, 1000, 700)
        bring_to_front(out)

        ctk.CTkLabel(
            out,
            text=f"Page Replacement ({res['algorithm']})",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=8)

        txt = ctk.CTkTextbox(out, width=960, height=560, wrap="none")
        txt.pack(padx=10, pady=6, fill="both", expand=True)
        txt.configure(font=("Courier New", 12))

        refs = res["references"]
        steps = res["steps"]
        frames = res["frames"]
        faults = res["page_faults"]
        hits = res["page_hits"]

        # ----- Column sizes -----
        cell_w = 5               # width of each value cell
        label_w = 10             # width for Frame0, Frame1 labels
        cw = lambda x: str(x).center(cell_w)

        # ----- Separator length -----
        sep_len = label_w + 1 + (len(refs) * (cell_w + 1))
        sep = "-" * sep_len + "\n"

        # ----- Header -----
        txt.insert("end", "References:".ljust(label_w) + " ")
        txt.insert("end", " ".join(cw(r) for r in refs) + "\n")
        txt.insert("end", sep)

        # ----- Build frames matrix -----
        frame_matrix = [[None for _ in steps] for _ in range(frames)]
        hf_row = []

        for t, st in enumerate(steps):
            snapshot = st["frames"]

            for fi in range(frames):
                frame_matrix[fi][t] = snapshot[fi] if fi < len(snapshot) else -1

            hf_row.append("F" if st["page_fault"] else "H")

        # ----- Print frames -----
        for fi in range(frames):
            label = f"Frame{fi}"
            row = " ".join(
                cw("-" if v == -1 else v) for v in frame_matrix[fi]
            )
            txt.insert("end", f"{label.ljust(label_w)} {row}\n")

        # ----- Result row -----
        txt.insert("end", sep)
        txt.insert("end", f"{'Result:'.ljust(label_w)} " + " ".join(cw(x) for x in hf_row) + "\n")

        # ----- Footer -----
        txt.insert("end", sep)
        txt.insert("end", f"Total Hits: {hits}    Total Faults: {faults}\n")

        txt.configure(state="disabled")

        def back():
            out.destroy()
            win.deiconify()

        ctk.CTkButton(out, text="Back to Input", command=back).pack(pady=8)

    # Run algorithm
    def run():
        try:
            refs = parse_refs(entry_refs.get())
            nframes = int(entry_frames.get())
            algo = algo_var.get()

            if nframes <= 0:
                raise ValueError("Frames must be > 0")
            if not refs:
                raise ValueError("Reference string is empty")
        except Exception as e:
            messagebox.showerror("Input error", str(e))
            return

        try:
            result = PageReplacement.simulate(refs, nframes, algo)
        except Exception as e:
            messagebox.showerror("Algorithm error", str(e))
            return

        show_output(result)

    win.mainloop()
