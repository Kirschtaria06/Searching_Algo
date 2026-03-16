import tkinter as tk
from tkinter import messagebox
import threading
import random
import time

# ================================================================
# ROOT
# ================================================================
root = tk.Tk()
root.title("Search Algorithm Visualizer")
root.configure(bg="#1e1e2e")
root.state("zoomed")

# ================================================================
# TOP BAR
# ================================================================
top_bar = tk.Frame(root, bg="#2a2a3e", pady=8)
top_bar.pack(side="top", fill="x")

controls = tk.Frame(top_bar, bg="#2a2a3e")
controls.pack(expand=True)

LABEL_FONT  = ("Segoe UI", 11)
ENTRY_FONT  = ("Segoe UI", 11)
BUTTON_FONT = ("Segoe UI", 11, "bold")
TIME_FONT   = ("Segoe UI", 11, "bold")
SUB_FONT    = ("Segoe UI", 9)
TOGGLE_FONT = ("Segoe UI", 9, "bold")

def lbl(parent, text, fg="#cdd6f4", font=LABEL_FONT, **kw):
    return tk.Label(parent, text=text, bg="#2a2a3e", fg=fg, font=font, **kw)

# ---- Inputs ----
lbl(controls, "Array Size:").grid(row=0, column=0, padx=(0, 4), rowspan=2, sticky="e")
array_size_var = tk.StringVar()
tk.Entry(controls, textvariable=array_size_var, width=6,
         font=ENTRY_FONT, bg="#313244", fg="#cdd6f4",
         insertbackground="white", relief="flat").grid(
    row=0, column=1, padx=(0, 16), rowspan=2, sticky="ns")

lbl(controls, "Search Value:").grid(row=0, column=2, padx=(0, 4), rowspan=2, sticky="e")
value_entry = tk.Entry(controls, width=6, font=ENTRY_FONT,
                       bg="#313244", fg="#cdd6f4",
                       insertbackground="white", relief="flat")
value_entry.grid(row=0, column=3, padx=(0, 16), rowspan=2, sticky="ns")

run_btn = tk.Button(controls, text="Run", font=BUTTON_FONT,
                    bg="#89b4fa", fg="#1e1e2e", relief="flat",
                    activebackground="#74c7ec", activeforeground="#1e1e2e",
                    padx=14, pady=4)
run_btn.grid(row=0, column=4, padx=(0, 20), rowspan=2)

# ---- Divider ----
tk.Frame(controls, bg="#585b70", width=2, height=44).grid(
    row=0, column=5, rowspan=2, padx=12)

# ---- Linear timing ----
lbl(controls, "Linear Search", fg="#a6e3a1", font=TIME_FONT).grid(
    row=0, column=6, padx=(0, 30), sticky="sw")
linear_time_label = lbl(controls, "—", fg="#a6e3a1", font=SUB_FONT)
linear_time_label.grid(row=1, column=6, padx=(0, 30), sticky="nw")

# ---- Divider ----
tk.Frame(controls, bg="#585b70", width=2, height=44).grid(
    row=0, column=7, rowspan=2, padx=12)

# ---- Binary mode toggle ----
binary_mode = tk.StringVar(value="presorted")  # "presorted" | "sortfirst"

def make_toggle_btn(parent, text, mode_val, col):
    def on_click():
        binary_mode.set(mode_val)
        refresh_toggle()
        apply_mode()
    b = tk.Button(parent, text=text, font=TOGGLE_FONT,
                  relief="flat", padx=8, pady=3, command=on_click)
    b.grid(row=0, column=col, padx=2)
    return b

toggle_frame = tk.Frame(controls, bg="#2a2a3e")
toggle_frame.grid(row=0, column=8, rowspan=2, padx=(0, 16))

lbl(toggle_frame, "Binary Mode:", fg="#cdd6f4", font=SUB_FONT).grid(
    row=0, column=0, columnspan=2, sticky="sw", pady=(0, 2))

btn_presorted = make_toggle_btn(toggle_frame, "Pre-sorted", "presorted", 0)
btn_sortfirst = make_toggle_btn(toggle_frame, "Sort first",  "sortfirst", 1)

def refresh_toggle():
    mode = binary_mode.get()
    btn_presorted.config(
        bg="#89dceb" if mode == "presorted" else "#313244",
        fg="#1e1e2e" if mode == "presorted" else "#cdd6f4")
    btn_sortfirst.config(
        bg="#f9e2af" if mode == "sortfirst" else "#313244",
        fg="#1e1e2e" if mode == "sortfirst" else "#cdd6f4")

refresh_toggle()

# ---- Divider ----
tk.Frame(controls, bg="#585b70", width=2, height=44).grid(
    row=0, column=9, rowspan=2, padx=12)

# ---- Binary timing area (swaps content based on mode) ----
binary_timing_frame = tk.Frame(controls, bg="#2a2a3e")
binary_timing_frame.grid(row=0, column=10, rowspan=2, sticky="w")

# Pre-sorted timing widgets
binary_title_label = lbl(binary_timing_frame, "Binary Search  (pre-sorted)",
                          fg="#89dceb", font=TIME_FONT)
binary_title_label.grid(row=0, column=0, columnspan=6, sticky="sw")

bp_time_label = lbl(binary_timing_frame, "—", fg="#89dceb", font=SUB_FONT)
bp_time_label.grid(row=1, column=0, sticky="nw")

# Sort-first timing widgets (hidden initially)
bs_sort_key   = lbl(binary_timing_frame, "Sort:",   fg="#fab387", font=SUB_FONT)
bs_sort_label = lbl(binary_timing_frame, "—",       fg="#fab387", font=SUB_FONT)
bs_srch_key   = lbl(binary_timing_frame, "Search:", fg="#f9e2af", font=SUB_FONT)
bs_srch_label = lbl(binary_timing_frame, "—",       fg="#f9e2af", font=SUB_FONT)
bs_tot_key    = lbl(binary_timing_frame, "Total:",  fg="#cba6f7", font=SUB_FONT)
bs_tot_label  = lbl(binary_timing_frame, "—",       fg="#cba6f7", font=SUB_FONT)

def show_presorted_timing():
    bs_sort_key.grid_remove();  bs_sort_label.grid_remove()
    bs_srch_key.grid_remove();  bs_srch_label.grid_remove()
    bs_tot_key.grid_remove();   bs_tot_label.grid_remove()
    bp_time_label.grid(row=1, column=0, sticky="nw", columnspan=2)

def show_sortfirst_timing():
    bp_time_label.grid_remove()
    bs_sort_key.grid(row=1, column=0, sticky="nw")
    bs_sort_label.grid(row=1, column=1, sticky="nw", padx=(2, 10))
    bs_srch_key.grid(row=1, column=2, sticky="nw")
    bs_srch_label.grid(row=1, column=3, sticky="nw", padx=(2, 10))
    bs_tot_key.grid(row=1, column=4, sticky="nw")
    bs_tot_label.grid(row=1, column=5, sticky="nw", padx=(2, 0))

# ================================================================
# CANVAS AREA  – always two panels
# ================================================================
canvas_area = tk.Frame(root, bg="#1e1e2e")
canvas_area.pack(side="top", fill="both", expand=True, padx=10, pady=(6, 10))
canvas_area.columnconfigure(0, weight=1, uniform="half")
canvas_area.columnconfigure(1, weight=1, uniform="half")
canvas_area.rowconfigure(0, weight=1)

TITLE_FONT = ("Segoe UI", 11, "bold")

def make_panel(parent, col, title, title_color):
    panel = tk.Frame(parent, bg="#181825")
    panel.grid(row=0, column=col, sticky="nsew",
               padx=(0, 5) if col == 0 else (5, 0))
    title_lbl = tk.Label(panel, text=title, bg="#181825", fg=title_color,
                          font=TITLE_FONT, pady=5)
    title_lbl.pack(fill="x")
    inner = tk.Frame(panel, bg="#181825")
    inner.pack(fill="both", expand=True)
    c = tk.Canvas(inner, bg="#0d0d1a", highlightthickness=0)
    c.pack(side="top", fill="both", expand=True)
    sb = tk.Scrollbar(inner, orient="horizontal", command=c.xview)
    sb.pack(side="bottom", fill="x")
    c.configure(xscrollcommand=sb.set)
    return c, title_lbl

canvas_linear, _              = make_panel(canvas_area, 0, "Linear Search  (unsorted)", "#a6e3a1")
canvas_binary, binary_panel_title = make_panel(canvas_area, 1, "Binary Search  (pre-sorted)", "#89dceb")

# ================================================================
# GLOBAL STATE
# ================================================================
array        = []
array_sorted = []

# ================================================================
# APPLY MODE  (update panel title + timing layout + redraw)
# ================================================================
def apply_mode():
    mode = binary_mode.get()
    if mode == "presorted":
        binary_panel_title.config(
            text="Binary Search  (pre-sorted)", fg="#89dceb")
        binary_title_label.config(
            text="Binary Search  (pre-sorted)", fg="#89dceb")
        show_presorted_timing()
        draw_array(canvas_binary, array_sorted)
    else:
        binary_panel_title.config(
            text="Binary Search  (insertion sort → search)", fg="#f9e2af")
        binary_title_label.config(
            text="Binary Search  (sort first)", fg="#f9e2af")
        show_sortfirst_timing()
        draw_array(canvas_binary, array)   # show unsorted state
    reset_binary_labels()

def reset_binary_labels():
    bp_time_label.config(text="—")
    bs_sort_label.config(text="—")
    bs_srch_label.config(text="—")
    bs_tot_label.config(text="—")

def reset_labels():
    linear_time_label.config(text="—")
    reset_binary_labels()

# ================================================================
# DRAW
# ================================================================
PADDING_TOP    = 24
PADDING_BOTTOM = 2
BAR_GAP        = 1

def draw_array(canvas, arr, left=None, right=None, mid=None, found_index=None):
    canvas.delete("all")
    n = len(arr)
    if n == 0:
        return
    cw = canvas.winfo_width()  or 400
    ch = canvas.winfo_height() or 300
    if cw < 2 or ch < 2:
        return

    drawable_h = ch - PADDING_TOP - PADDING_BOTTOM
    max_val    = max(arr)
    bar_w      = max(4, (cw - BAR_GAP) // n - BAR_GAP)
    total_w    = n * (bar_w + BAR_GAP) + BAR_GAP
    offset_x   = max(0, (cw - total_w) // 2)

    canvas.config(scrollregion=(0, 0, max(cw, total_w), ch))
    show_labels = bar_w >= 18

    for i, val in enumerate(arr):
        x0 = offset_x + i * (bar_w + BAR_GAP)
        x1 = x0 + bar_w
        bar_h = max(1, int(val / max_val * drawable_h))
        y1 = ch - PADDING_BOTTOM
        y0 = y1 - bar_h

        if found_index == i:
            color = "#a6e3a1"
        elif mid == i:
            color = "#f9e2af"
        elif left is not None and right is not None and (i < left or i > right):
            color = "#45475a"
        else:
            color = "#cdd6f4"

        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
        if show_labels:
            canvas.create_text(x0 + bar_w // 2, y0 - 10,
                                text=str(val), fill="#f38ba8",
                                font=("Segoe UI", 8, "bold"))
    canvas.update_idletasks()

# ================================================================
# ARRAY GENERATION
# ================================================================
def update_array(*args):
    global array, array_sorted
    raw = array_size_var.get().strip()
    if not raw:
        array = array_sorted = []
        draw_array(canvas_linear, [])
        draw_array(canvas_binary, [])
        reset_labels()
        return
    try:
        size = max(1, int(raw))
    except ValueError:
        return

    array        = list(range(1, size + 1))
    random.shuffle(array)
    array_sorted = sorted(array)

    draw_array(canvas_linear, array)
    apply_mode()   # draws binary canvas in the correct state
    reset_labels()

array_size_var.trace_add("write", update_array)

# ================================================================
# ALGORITHMS
# ================================================================
def linear_search_timed(arr, target):
    algo_time = 0.0
    for i, val in enumerate(arr):
        draw_array(canvas_linear, arr, mid=i)
        time.sleep(0.05)
        t0 = time.perf_counter()
        found = val == target
        algo_time += time.perf_counter() - t0
        if found:
            draw_array(canvas_linear, arr, found_index=i)
            return i, algo_time
    return -1, algo_time


def insertion_sort_timed(arr):
    a = arr[:]
    n = len(a)
    SLEEP = max(0.005, 0.08 - n * 0.001)
    algo_time = 0.0
    for i in range(1, n):
        key = a[i]
        j = i - 1
        t0 = time.perf_counter()
        cond = j >= 0 and a[j] > key
        algo_time += time.perf_counter() - t0
        while cond:
            a[j + 1] = a[j]
            j -= 1
            draw_array(canvas_binary, a, mid=j + 1)
            time.sleep(SLEEP)
            t0 = time.perf_counter()
            cond = j >= 0 and a[j] > key
            algo_time += time.perf_counter() - t0
        t0 = time.perf_counter()
        a[j + 1] = key
        algo_time += time.perf_counter() - t0
        draw_array(canvas_binary, a, mid=j + 1)
    draw_array(canvas_binary, a)
    return a, algo_time


def binary_search_timed(arr_s, target):
    left, right = 0, len(arr_s) - 1
    algo_time = 0.0
    while left <= right:
        t0 = time.perf_counter()
        mid = (left + right) // 2
        algo_time += time.perf_counter() - t0
        draw_array(canvas_binary, arr_s, left=left, right=right, mid=mid)
        time.sleep(0.1)
        t0 = time.perf_counter()
        if arr_s[mid] == target:
            algo_time += time.perf_counter() - t0
            draw_array(canvas_binary, arr_s, found_index=mid)
            return mid, algo_time
        elif arr_s[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
        algo_time += time.perf_counter() - t0
    return -1, algo_time

# ================================================================
# RUN
# ================================================================
def start_algorithm():
    global array, array_sorted
    if not array:
        messagebox.showinfo("Notice", "Enter an array size first.")
        return
    raw = value_entry.get().strip()
    if not raw:
        messagebox.showinfo("Notice", "Please enter a value to search!")
        return
    try:
        target = int(raw)
    except ValueError:
        messagebox.showerror("Input Error", "Search value must be an integer.")
        return
    if target < 1 or target > len(array):
        messagebox.showerror("Input Error",
                             f"Value must be between 1 and {len(array)}.")
        return

    run_btn.config(state="disabled")
    linear_time_label.config(text="running…")
    reset_binary_labels()

    mode = binary_mode.get()

    def run():
        # ── Linear ──────────────────────────────────────────────
        _, lin_s = linear_search_timed(array, target)
        linear_time_label.config(text=f"{lin_s * 1000:.4f} ms")

        # ── Binary: pre-sorted ───────────────────────────────────
        if mode == "presorted":
            bp_time_label.config(text="searching…")
            draw_array(canvas_binary, array_sorted)
            _, pre_s = binary_search_timed(array_sorted, target)
            bp_time_label.config(text=f"{pre_s * 1000:.4f} ms")

        # ── Binary: sort first ───────────────────────────────────
        else:
            draw_array(canvas_binary, array)
            bs_sort_label.config(text="sorting…")
            arr_ins, sort_s = insertion_sort_timed(array)
            bs_sort_label.config(text=f"{sort_s * 1000:.4f} ms")

            bs_srch_label.config(text="searching…")
            _, srch_s = binary_search_timed(arr_ins, target)
            bs_srch_label.config(text=f"{srch_s * 1000:.4f} ms")
            bs_tot_label.config(text=f"{(sort_s + srch_s) * 1000:.4f} ms")

        run_btn.config(state="normal")

    threading.Thread(target=run, daemon=True).start()

run_btn.config(command=start_algorithm)

# ================================================================
# RESIZE
# ================================================================
_resize_id = None
def on_resize(event):
    global _resize_id
    if event.widget is not root:
        return
    if _resize_id:
        root.after_cancel(_resize_id)
    def redraw():
        draw_array(canvas_linear, array)
        if binary_mode.get() == "presorted":
            draw_array(canvas_binary, array_sorted)
        else:
            draw_array(canvas_binary, array)
    _resize_id = root.after(80, redraw)

root.bind("<Configure>", on_resize)

# ================================================================
# BOOT
# ================================================================
update_array()
root.mainloop()