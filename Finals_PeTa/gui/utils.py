# Minimal GUI utility helpers.

import random

def center_window(root, width=1200, height=700):
    # Center the window 
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

def bring_to_front(win):
    # Open new window in front of the previous one
    try:
        win.lift()
        win.after(50, lambda: win.focus_force())
        win.attributes("-topmost", True)
        win.after(200, lambda: win.attributes("-topmost", False))
    except Exception:
        try:
            win.lift()
            win.focus_force()
        except Exception:
            pass

def animate_entry(entry, final_value, delay=40, steps=8, min_val=0, max_val=15):
    # Auto Generate Animation
    def step(count):
        if count > 0:
            entry.delete(0, "end")
            entry.insert(0, str(random.randint(min_val, max_val)))
            entry.after(delay, step, count - 1)
        else:
            entry.delete(0, "end")
            entry.insert(0, str(final_value))
    step(steps)

def animate_text(entry, final_text, delay=40, steps=8):
    parts = final_text.split()
    def step(count):
        if count > 0:
            fake = [str(random.randint(0, max(9, int(p) if p.isdigit() else 9))) for p in parts]
            entry.delete(0, "end")
            entry.insert(0, " ".join(fake))
            entry.after(delay, step, count - 1)
        else:
            entry.delete(0, "end")
            entry.insert(0, final_text)
    step(steps)
