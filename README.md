# Search Algorithm Visualizer

An interactive desktop application that visualizes and compares **Linear Search** and **Binary Search** side by side in real time, built with Python and Tkinter.

---

## Features

- **Two-panel layout** — Linear Search on the left, Binary Search on the right, both filling the full window
- **Toggleable Binary Search mode** — switch between two variants without restarting:
  - **Pre-sorted** — the array is already sorted before the search begins; shows pure search cost only
  - **Sort first** — starts from a shuffled array, plays an insertion sort animation, then searches; shows Sort time, Search time, and Total separately
- **Honest timing** — `time.perf_counter()` is used to measure only the algorithmic work; `time.sleep()` animation delays are excluded from all reported times
- **Values 1 to N** — the array always contains every integer from 1 to the chosen size exactly once, so any value you type is guaranteed to exist
- **Responsive layout** — panels resize and redraw automatically as the window is resized
- **Scrollable canvases** — handles large arrays cleanly with a horizontal scrollbar
- **Value labels** — shown above bars when bars are wide enough (≥ 18 px)

### Color Legend

| Color | Meaning |
|---|---|
| White | Unvisited element |
| Yellow | Current element being examined |
| Gray | Eliminated range (Binary Search only) |
| Green | Found — target located |

---

## Requirements

- Python 3.7 or higher
- Tkinter (included with most Python installations)

No third-party packages are required.

### Checking Tkinter

```bash
python -m tkinter
```

A small test window should appear. If it does not, install Tkinter for your platform:

```bash
# Ubuntu / Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS (via Homebrew)
brew install python-tk
```

---

## Installation

```bash
git clone https://github.com/your-username/search-visualizer.git
cd search-visualizer
```

No additional installation steps are needed.

---

## Usage

```bash
python search_visualizer.py
```

1. Enter an **Array Size** (e.g. `30`) — the array regenerates automatically as you type
2. Choose a **Binary Mode** using the toggle buttons:
   - **Pre-sorted** for a fair search-only comparison
   - **Sort first** to see the full cost including sorting
3. Enter a **Search Value** between 1 and your chosen array size
4. Click **Run** — both algorithms animate simultaneously across the two panels
5. Timing results appear in the top bar as each phase completes

---

## Understanding the Timings

### Linear Search
Scans the unsorted array from left to right, one element at a time. Time shown is the pure comparison cost.

### Binary Search — Pre-sorted mode
Operates on a copy of the array that was sorted at generation time (not during the run). The time shown reflects only the binary search itself — no sorting overhead. This is the fairest way to compare the two search algorithms head-to-head.

### Binary Search — Sort first mode
Starts from the same shuffled array that Linear Search uses. It runs an **insertion sort** animation to sort the array first, then performs the binary search. Three times are shown:

| Label | What it measures |
|---|---|
| **Sort** | Insertion sort comparisons and swaps only (animation delays excluded) |
| **Search** | Binary search comparisons only |
| **Total** | Sort + Search combined |

This mode illustrates an important real-world point: binary search is only worthwhile if your data is already sorted or will be searched many times. On small arrays, the sort overhead alone can exceed the total time of a linear search.

---

## Algorithm Complexity

| Algorithm | Best | Average | Worst | Requires sorted data? |
|---|---|---|---|---|
| Linear Search | O(1) | O(n) | O(n) | No |
| Binary Search | O(1) | O(log n) | O(log n) | Yes |
| Insertion Sort | O(n) | O(n²) | O(n²) | — |

Binary search is dramatically faster for large arrays — but only once the data is sorted. The **Sort first** mode makes this trade-off visible and measurable.

---

## Project Structure

```
search-visualizer/
└── search_visualizer.py    # Single-file application — no dependencies
```

---

## Tips

- Try a **small array (≤ 15)** with Sort first mode to clearly see each insertion sort swap
- Try a **large array (≥ 60)** with Pre-sorted mode to see binary search finish in just a handful of steps while linear search is still scanning
- Change the array size between runs to generate a new shuffled array automatically
- The Run button is disabled during execution to prevent overlapping animations

---

## License

MIT License — free to use, modify, and distribute.
