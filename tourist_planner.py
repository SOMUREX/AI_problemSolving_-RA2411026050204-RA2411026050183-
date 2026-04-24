"""
Tourist Travel Planner — TSP
Python/Matplotlib port of tourist_planner.html

Click on the map to add destinations, then solve with Brute Force or Nearest Neighbor.
Run:  python tourist_planner.py
"""

import math
import time
import itertools
import matplotlib
matplotlib.use("TkAgg") if False else None   # auto-detect backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import Button, TextBox
from matplotlib.lines import Line2D

# ── Palette (mirrors the warm parchment theme) ──────────────────────────────
BG          = "#f0ebe1"
SURFACE     = "#faf7f0"
CARD        = "#ffffff"
BORDER      = "#ddd5c4"
TEXT        = "#2c1810"
MUTED       = "#8b7355"
ACCENT      = "#c0392b"   # red  – brute force
ACCENT2     = "#2980b9"   # blue
ACCENT3     = "#27ae60"   # green – nearest neighbor

PIN_COLORS  = ["#c0392b","#2980b9","#27ae60","#8e44ad",
               "#f39c12","#16a085","#d35400","#2c3e50","#e91e63"]

# ── State ────────────────────────────────────────────────────────────────────
destinations = []   # list of {"name": str, "x": float, "y": float}
brute_result = None
nn_result    = None

# ── Geometry ─────────────────────────────────────────────────────────────────

def dist(a, b):
    return math.sqrt((a["x"]-b["x"])**2 + (a["y"]-b["y"])**2)

def route_len(order):
    n = len(order)
    return sum(dist(destinations[order[i]], destinations[order[(i+1)%n]])
               for i in range(n))

# ── Algorithms ───────────────────────────────────────────────────────────────

def solve_brute():
    global brute_result
    if len(destinations) < 3:
        return
    t0 = time.perf_counter()
    rest = list(range(1, len(destinations)))
    best, best_order, count = math.inf, None, 0
    for perm in itertools.permutations(rest):
        order = [0] + list(perm)
        d = route_len(order)
        count += 1
        if d < best:
            best, best_order = d, order
    elapsed = (time.perf_counter() - t0) * 1000
    brute_result = {"order": best_order, "dist": best,
                    "routes": count, "ms": elapsed}
    refresh()

def solve_nn():
    global nn_result
    if len(destinations) < 3:
        return
    t0 = time.perf_counter()
    visited, order = {0}, [0]
    while len(order) < len(destinations):
        last = order[-1]
        nearest, nd = -1, math.inf
        for i in range(len(destinations)):
            if i not in visited:
                d = dist(destinations[last], destinations[i])
                if d < nd:
                    nd, nearest = d, i
        visited.add(nearest)
        order.append(nearest)
    total = route_len(order)
    elapsed = (time.perf_counter() - t0) * 1000
    nn_result = {"order": order, "dist": total, "ms": elapsed}
    refresh()

# ── Drawing ──────────────────────────────────────────────────────────────────

def draw_map():
    ax_map.cla()
    ax_map.set_facecolor(SURFACE)
    ax_map.set_xlim(0, 1); ax_map.set_ylim(0, 1)
    ax_map.tick_params(left=False, bottom=False,
                       labelleft=False, labelbottom=False)
    for spine in ax_map.spines.values():
        spine.set_edgecolor(BORDER)

    # Grid
    for v in [i/10 for i in range(1,10)]:
        ax_map.axvline(v, color=BORDER, linewidth=0.5, alpha=0.6)
        ax_map.axhline(v, color=BORDER, linewidth=0.5, alpha=0.6)

    # NN route (green dashed)
    if nn_result:
        o = nn_result["order"]
        xs = [destinations[o[i % len(o)]]["x"] for i in range(len(o)+1)]
        ys = [destinations[o[i % len(o)]]["y"] for i in range(len(o)+1)]
        ax_map.plot(xs, ys, color=ACCENT3, linewidth=2, linestyle="--",
                    alpha=0.55, zorder=2)

    # Brute force route (red solid)
    if brute_result:
        o = brute_result["order"]
        xs = [destinations[o[i % len(o)]]["x"] for i in range(len(o)+1)]
        ys = [destinations[o[i % len(o)]]["y"] for i in range(len(o)+1)]
        ax_map.plot(xs, ys, color=ACCENT, linewidth=2.5,
                    alpha=0.8, zorder=3)

    # Pins
    for i, d in enumerate(destinations):
        color = PIN_COLORS[i % len(PIN_COLORS)]
        circle = plt.Circle((d["x"], d["y"]), 0.025,
                             color=color, zorder=5, linewidth=2,
                             ec="white")
        ax_map.add_patch(circle)
        # Number label inside pin
        ax_map.text(d["x"], d["y"], str(i+1),
                    ha="center", va="center",
                    fontsize=7, fontweight="bold", color="white", zorder=6)
        # Name below
        ax_map.text(d["x"], d["y"]-0.045, d["name"],
                    ha="center", va="top",
                    fontsize=7, fontweight="600", color=TEXT, zorder=6)
        # Star for first city
        if i == 0:
            ax_map.text(d["x"]+0.035, d["y"]+0.03, "★",
                        fontsize=10, color="#f39c12", zorder=7)

    # Legend
    legend_items = []
    if brute_result:
        legend_items.append(Line2D([0],[0], color=ACCENT, lw=2.5,
                                   label=f'Brute Force — {brute_result["dist"]:.0f} km'))
    if nn_result:
        legend_items.append(Line2D([0],[0], color=ACCENT3, lw=2,
                                   linestyle="--",
                                   label=f'Nearest Neighbor — {nn_result["dist"]:.0f} km'))
    if legend_items:
        ax_map.legend(handles=legend_items, loc="upper right",
                      fontsize=7, framealpha=0.9,
                      facecolor=CARD, edgecolor=BORDER)

    ax_map.set_title("Click on map to add destinations  ✈",
                     fontsize=9, color=MUTED, pad=6)


def draw_itinerary():
    ax_itin.cla()
    ax_itin.axis("off")
    ax_itin.set_facecolor(CARD)

    y = 0.97
    ax_itin.text(0.5, y, "✈  ITINERARY",
                 ha="center", va="top", fontsize=10,
                 fontweight="bold", color=TEXT,
                 transform=ax_itin.transAxes)
    y -= 0.09

    result, algo_label, color = None, "", ACCENT
    if brute_result:
        result = brute_result
        algo_label = "Brute Force (Optimal)"
        color = ACCENT
    elif nn_result:
        result = nn_result
        algo_label = "Nearest Neighbor"
        color = ACCENT3

    if result is None:
        ax_itin.text(0.5, 0.5, "Solve a route to\nsee itinerary",
                     ha="center", va="center", fontsize=9,
                     color=MUTED, transform=ax_itin.transAxes, alpha=0.7)
        fig.canvas.draw_idle()
        return

    ax_itin.text(0.5, y, algo_label,
                 ha="center", va="top", fontsize=8,
                 color=color, fontstyle="italic",
                 transform=ax_itin.transAxes)
    y -= 0.10

    order = result["order"]
    n = len(order)
    row_h = min(0.09, 0.75 / n)

    for i in range(n):
        frm = destinations[order[i]]
        to  = destinations[order[(i+1) % n]]
        d   = dist(frm, to)
        pin_col = PIN_COLORS[order[i] % len(PIN_COLORS)]

        # Numbered badge
        badge = plt.Circle((0.07, y - row_h*0.35), 0.025,
                            color=pin_col, transform=ax_itin.transAxes,
                            clip_on=False)
        ax_itin.add_patch(badge)
        ax_itin.text(0.07, y - row_h*0.35, str(i+1),
                     ha="center", va="center", fontsize=6,
                     color="white", fontweight="bold",
                     transform=ax_itin.transAxes)

        ax_itin.text(0.16, y - row_h*0.3,
                     f"{frm['name']}  →  {to['name']}",
                     va="center", fontsize=7.5, color=TEXT,
                     transform=ax_itin.transAxes)
        ax_itin.text(0.95, y - row_h*0.3,
                     f"{d:.0f} km",
                     va="center", ha="right", fontsize=7,
                     color=MUTED, transform=ax_itin.transAxes)

        ax_itin.axhline(y - row_h*0.78, xmin=0.04, xmax=0.96,
                        color=BORDER, linewidth=0.5,
                        transform=ax_itin.transAxes)
        y -= row_h

    # Total bar
    y -= 0.02
    total_rect = mpatches.FancyBboxPatch(
        (0.04, y-0.08), 0.92, 0.075,
        boxstyle="round,pad=0.01",
        facecolor=ACCENT, edgecolor="none",
        transform=ax_itin.transAxes, clip_on=False)
    ax_itin.add_patch(total_rect)
    ax_itin.text(0.08, y-0.045, "TOTAL DISTANCE",
                 va="center", fontsize=7.5, color="white",
                 fontweight="bold", transform=ax_itin.transAxes)
    ax_itin.text(0.96, y-0.045, f"{result['dist']:.0f} km",
                 va="center", ha="right", fontsize=8,
                 color="white", fontweight="bold",
                 transform=ax_itin.transAxes)

    # Comparison
    if brute_result and nn_result:
        y -= 0.12
        ax_itin.text(0.5, y, "COMPARISON",
                     ha="center", va="top", fontsize=8,
                     fontweight="bold", color=TEXT,
                     transform=ax_itin.transAxes)
        y -= 0.09
        ax_itin.text(0.25, y, f"Brute Force\n{brute_result['dist']:.0f} km",
                     ha="center", va="top", fontsize=8,
                     color=ACCENT, fontweight="bold",
                     transform=ax_itin.transAxes)
        ax_itin.text(0.75, y, f"Nearest Neighbor\n{nn_result['dist']:.0f} km",
                     ha="center", va="top", fontsize=8,
                     color=ACCENT3, fontweight="bold",
                     transform=ax_itin.transAxes)

    fig.canvas.draw_idle()


def draw_dest_list():
    ax_list.cla()
    ax_list.axis("off")
    ax_list.set_facecolor(CARD)
    ax_list.text(0.5, 0.97, "DESTINATIONS",
                 ha="center", va="top", fontsize=9,
                 fontweight="bold", color=TEXT,
                 transform=ax_list.transAxes)

    if not destinations:
        ax_list.text(0.5, 0.5, "No destinations yet…\nClick the map!",
                     ha="center", va="center", fontsize=8,
                     color=MUTED, transform=ax_list.transAxes, alpha=0.7)
    else:
        row_h = min(0.1, 0.85 / len(destinations))
        y = 0.87
        for i, d in enumerate(destinations):
            color = PIN_COLORS[i % len(PIN_COLORS)]
            badge = plt.Circle((0.12, y), 0.055,
                               color=color, transform=ax_list.transAxes,
                               clip_on=False)
            ax_list.add_patch(badge)
            ax_list.text(0.12, y, str(i+1),
                         ha="center", va="center", fontsize=7,
                         color="white", fontweight="bold",
                         transform=ax_list.transAxes)
            ax_list.text(0.25, y, d["name"],
                         va="center", fontsize=8, color=TEXT,
                         transform=ax_list.transAxes)
            y -= row_h + 0.04

    fig.canvas.draw_idle()


def refresh():
    draw_map()
    draw_dest_list()
    draw_itinerary()
    fig.canvas.draw_idle()

# ── Interaction ───────────────────────────────────────────────────────────────

def on_click(event):
    if event.inaxes != ax_map:
        return
    if event.button != 1:
        return
    name = tb_name.text.strip() or f"Stop {len(destinations)+1}"
    tb_name.set_val("")
    if len(destinations) >= 9:
        ax_map.set_title("Max 9 destinations!", color=ACCENT, fontsize=9)
        fig.canvas.draw_idle()
        return
    destinations.append({"name": name, "x": event.xdata, "y": event.ydata})
    global brute_result, nn_result
    brute_result = nn_result = None
    refresh()

def btn_brute_cb(event):
    global brute_result, nn_result
    nn_result = None
    solve_brute()

def btn_nn_cb(event):
    global brute_result, nn_result
    brute_result = None
    solve_nn()

def btn_both_cb(event):
    global brute_result, nn_result
    brute_result = nn_result = None
    solve_brute()
    solve_nn()

def btn_preset_cb(event):
    global destinations, brute_result, nn_result
    destinations = [
        {"name": "Home Base",        "x": 0.50, "y": 0.50},
        {"name": "Eiffel Tower",     "x": 0.20, "y": 0.80},
        {"name": "Colosseum",        "x": 0.70, "y": 0.75},
        {"name": "Acropolis",        "x": 0.80, "y": 0.40},
        {"name": "Sagrada Familia",  "x": 0.15, "y": 0.35},
        {"name": "Big Ben",          "x": 0.30, "y": 0.85},
    ]
    brute_result = nn_result = None
    refresh()

def btn_reset_cb(event):
    global destinations, brute_result, nn_result
    destinations = []
    brute_result = nn_result = None
    refresh()

# ── Layout ────────────────────────────────────────────────────────────────────

fig = plt.figure(figsize=(14, 8), facecolor=BG)
fig.suptitle("✈  Tourist Travel Planner  —  TSP",
             fontsize=16, fontweight="bold", color=ACCENT,
             fontfamily="serif", y=0.97)

# Axes: [left, bottom, width, height]
ax_list  = fig.add_axes([0.01, 0.22, 0.16, 0.70], facecolor=CARD)
ax_map   = fig.add_axes([0.19, 0.22, 0.50, 0.70], facecolor=SURFACE)
ax_itin  = fig.add_axes([0.71, 0.22, 0.28, 0.70], facecolor=CARD)

# Add a thin border rectangle to each panel
for ax in (ax_list, ax_map, ax_itin):
    for spine in ax.spines.values():
        spine.set_edgecolor(BORDER)
        spine.set_linewidth(1.2)

# TextBox — destination name
ax_tb = fig.add_axes([0.01, 0.13, 0.16, 0.055])
tb_name = TextBox(ax_tb, "", initial="Type name, then click map",
                  color=SURFACE, hovercolor="#eef5fb")
tb_name.label.set_fontsize(0)

# Buttons row
btn_specs = [
    ([0.01,  0.07, 0.075, 0.048], "⚡ Brute Force",     ACCENT,  "white", btn_brute_cb),
    ([0.095, 0.07, 0.075, 0.048], "🧭 Nearest Nbr",     ACCENT3, "white", btn_nn_cb),
    ([0.01,  0.02, 0.075, 0.038], "★  Load Preset",     ACCENT2, "white", btn_preset_cb),
    ([0.095, 0.02, 0.075, 0.038], "⟳  Reset All",       SURFACE, TEXT,   btn_reset_cb),
    ([0.19,  0.07, 0.12,  0.048], "⚡+🧭  Solve Both",  "#8e44ad","white", btn_both_cb),
]

for rect, label, bg, fg, cb in btn_specs:
    ax_b = fig.add_axes(rect)
    btn = Button(ax_b, label, color=bg, hovercolor=bg)
    btn.label.set_color(fg)
    btn.label.set_fontsize(8.5)
    btn.label.set_fontweight("bold")
    btn.on_clicked(cb)
    # keep reference so GC doesn't collect it
    ax_b._btn = btn

fig.canvas.mpl_connect("button_press_event", on_click)

# Initial draw
refresh()
plt.show()
