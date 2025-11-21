#!/usr/bin/env python3
import tkinter as tk
from tkinter import Scale

# ---------------------------
MARGIN = 10  # Margin around tile


def update_color(*args):
    """Update tile color from slider values."""
    r = r_scale.get()
    g = g_scale.get()
    b = b_scale.get()
    color = f"#{r:02x}{g:02x}{b:02x}"
    canvas.itemconfig(tile, fill=color)


def resize_tile(event):
    """Resize tile when canvas size changes, keeping margin."""
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    side = min(w, h) - 2 * MARGIN
    side = max(side, 10)  # prevent zero or negative

    x0 = (w - side) // 2
    y0 = (h - side) // 2
    x1 = x0 + side
    y1 = y0 + side

    canvas.coords(tile, x0, y0, x1, y1)


# ---------------------------
# --- Main Application Setup ---

root = tk.Tk()
root.title("RGB Colour Tile")
root.geometry("1000x700")

# Outer frame with padding
outer = tk.Frame(root, padx=MARGIN, pady=MARGIN)
outer.pack(fill="both", expand=True)

# ---- Canvas for tile ----
canvas = tk.Canvas(outer, bg="gray20", highlightthickness=0)
canvas.grid(row=0, column=0, sticky="nsew")

# Configure grid to expand canvas
outer.columnconfigure(0, weight=1)
outer.rowconfigure(0, weight=1)

# Initial tile color = white
tile = canvas.create_rectangle(0, 0, 100, 100, fill="#ffffff", outline="")

# Bind resize event
canvas.bind("<Configure>", resize_tile)

# ---- Sliders column ----
sliders = tk.Frame(outer, padx=10)
sliders.grid(row=0, column=1, sticky="ns")

r_scale = Scale(
    sliders,
    from_=0,
    to=255,
    orient=tk.VERTICAL,
    label="R",
    command=update_color
)
r_scale.set(255)
r_scale.pack(pady=10)

g_scale = Scale(
    sliders,
    from_=0,
    to=255,
    orient=tk.VERTICAL,
    label="G",
    command=update_color
)
g_scale.set(255)
g_scale.pack(pady=10)

b_scale = Scale(
    sliders,
    from_=0,
    to=255,
    orient=tk.VERTICAL,
    label="B",
    command=update_color
)
b_scale.set(255)
b_scale.pack(pady=10)

root.mainloop()
