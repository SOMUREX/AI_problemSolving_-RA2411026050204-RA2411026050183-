"""
Logistics Route Optimizer — TSP
Python/Matplotlib port of logistics_tsp.html

Dark industrial theme. Click map to add cities, solve with Brute Force or Nearest Neighbor.
Run:  python logistics_tsp.py
"""

import math
import time
import itertools
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import Button, TextBox
from matplotlib.lines import Line2D

# ── Palette (mirrors the dark industrial theme) ──────────────────────────────
BG       = "#0f1117"
PANEL    = "#161b27"
CARD     = "#1c2333"
BORDER   = "#2a3347"
ACCENT   = "#f5a623"    # orange – brute force
ACCENT2  = "#00d4aa"    # teal   – nearest neighbor
ACCENT3  = "#ff4757"    # red    – delete / reset
TEXT     = "#e8eaf0"
MUTED    = "#6b7a99"

CITY_COLORS = ["#f5a623","#00d4aa","#ff4757","#a29bfe",
               "#fd79a8","#55efc4","#fdcb6e","#e17055",
               "#74b9ff","#b2bec3"]

# ── State ────────────────────────────────────────────────────────────────────
cities      = []
brute_route = None
heur_route  = None

# ── Geometry ─────────────────────────────────────────────────────────────────

def dist(a, b):
    return math.sqrt((a["x"]-b["x"])**2 + (a["y"]-b["y"])**2)

def route_length(order):
    n = len(order)
    return sum(dist(cities[order[i]], cities[order[(i+1) % n]])
               for i in range(n))

# ── Algorithms ───────────────────────────────────────────────────────────────

def solve_brute():
    global brute_route
    if len(cities) < 3:
        return
    t0 = time.perf_counter()
    rest = list(range(1, len(cities)))
    best, best_order, count = math.inf, None, 0
    for perm in itertools.permutations(rest):
        order = [0] + list(perm)
        d = route_length(order)
        count += 1
        if d < best:
            best, best_order = d, order
    elapsed = (time.perf_counter() - t0) * 1000
    brute_route = {"order": best_order, "dist": best,
                   "routes": count, "ms": elapsed}
    refresh()

def solve_heuristic():
    global heur_route
    if len(cities) < 3:
        return
    t0 = time.perf_counter()
    visited, order, comparisons = {0}, [0], 0
    while len(order) < len(cities):
        last = order[-1]
        nearest, nd = -1, math.inf
        for i in range(len(cities)):
            comparisons += 1
            if i not in visited:
                d = dist(cities[last], cities[i])
                if d < nd:
                    nd, nearest = d, i
        visited.add(nearest)
        order.append(nearest)
    total = route_length(order)
    elapsed = (time.perf_counter() - t0) * 1000
    heur_route = {"order": order, "dist": total,
                  "comparisons": comparisons, "ms": elapsed}
    refresh()

# ── Drawing ───────────────────────────────────────────────────────────────────

def draw_map():
    ax_map.cla()
    ax_map.set_facecolor(PANEL)
    ax_map.set_xlim(0, 1); ax_map.set_ylim(0, 1)
    ax_map.tick_params(left=False, bottom=False,
                       labelleft=False, labelbottom=False)
    for spine in ax_map.spines.values():
        spine.set_edgecolor(BORDER)

    # Grid (matches the CSS background-image grid)
    for v in [i/10 for i in range(1,10)]:
        ax_map.axvline(v, color=ACCENT, linewidth=0.3, alpha=0.15)
        ax_map.axhline(v, color=ACCENT, linewidth=0.3, alpha=0.15)

    # Brute force route (orange solid)
    if brute_route:
        o = brute_route["order"]
        xs = [cities[o[i % len(o)]]["x"] for i in range(len(o)+1)]
        ys = [cities[o[i % len(o)]]["y"] for i in range(len(o)+1)]
        ax_map.plot(xs, ys, color=ACCENT, linewidth=2.5,
                    alpha=0.75, zorder=2)

    # Heuristic route (teal dashed)
    if heur_route:
        o = heur_route["order"]
        xs = [cities[o[i % len(o)]]["x"] for i in range(len(o)+1)]
        ys = [cities[o[i % len(o)]]["y"] for i in range(len(o)+1)]
        ax_map.plot(xs, ys, color=ACCENT2, linewidth=2,
                    linestyle="--", alpha=0.7, zorder=3)

    # City nodes
    for i, c in enumerate(cities):
        color = CITY_COLORS[i % len(CITY_COLORS)]
        circle = plt.Circle((c["x"], c["y"]), 0.022,
                             color=color, zorder=5,
                             ec=BG, linewidth=2)
        ax_map.add_patch(circle)
        ax_map.text(c["x"], c["y"], str(i+1),
                    ha="center", va="center",
                    fontsize=6.5, fontweight="bold",
                    color=BG, zorder=6,
                    fontfamily="monospace")
        ax_map.text(c["x"], c["y"]-0.04, c["name"],
                    ha="center", va="top",
                    fontsize=7, color=TEXT, zorder=6,
                    fontfamily="monospace")

    # Legend
    legend_items = []
    if brute_route:
        legend_items.append(Line2D([0],[0], color=ACCENT, lw=2.5,
                                   label=f'⚡ Brute Force  {brute_route["dist"]:.0f} units'))
    if heur_route:
        legend_items.append(Line2D([0],[0], color=ACCENT2, lw=2,
                                   linestyle="--",
                                   label=f'🧭 Nearest Nbr  {heur_route["dist"]:.0f} units'))
    if legend_items:
        leg = ax_map.legend(handles=legend_items, loc="upper right",
                            fontsize=7.5, framealpha=0.85,
                            facecolor=CARD, edgecolor=BORDER,
                            labelcolor=TEXT)

    ax_map.set_title("CLICK MAP TO PLACE CITIES",
                     fontsize=8, color=MUTED,
                     fontfamily="monospace", pad=6)


def draw_city_list():
    ax_list.cla()
    ax_list.axis("off")
    ax_list.set_facecolor(CARD)
    ax_list.text(0.5, 0.97, "CITY LIST",
                 ha="center", va="top", fontsize=9,
                 fontweight="bold", color=ACCENT,
                 fontfamily="monospace",
                 transform=ax_list.transAxes)

    if not cities:
        ax_list.text(0.5, 0.5, "No cities yet.\nClick the map!",
                     ha="center", va="center", fontsize=8,
                     color=MUTED, fontfamily="monospace",
                     transform=ax_list.transAxes, alpha=0.7)
    else:
        row_h = min(0.09, 0.82 / len(cities))
        y = 0.87
        for i, c in enumerate(cities):
            color = CITY_COLORS[i % len(CITY_COLORS)]
            dot = plt.Circle((0.10, y), 0.038,
                             color=color, transform=ax_list.transAxes,
                             clip_on=False)
            ax_list.add_patch(dot)
            ax_list.text(0.10, y, str(i+1),
                         ha="center", va="center", fontsize=6.5,
                         color=BG, fontweight="bold",
                         fontfamily="monospace",
                         transform=ax_list.transAxes)
            ax_list.text(0.24, y, c["name"],
                         va="center", fontsize=8, color=TEXT,
                         fontfamily="monospace",
                         transform=ax_list.transAxes)
            y -= row_h + 0.04

    fig.canvas.draw_idle()


def draw_results():
    ax_res.cla()
    ax_res.axis("off")
    ax_res.set_facecolor(CARD)

    ax_res.text(0.5, 0.97, "RESULTS",
                ha="center", va="top", fontsize=9,
                fontweight="bold", color=ACCENT,
                fontfamily="monospace",
                transform=ax_res.transAxes)

    if brute_route is None and heur_route is None:
        ax_res.text(0.5, 0.5, "Run an algorithm\nto see results",
                    ha="center", va="center", fontsize=8,
                    color=MUTED, fontfamily="monospace",
                    transform=ax_res.transAxes, alpha=0.7)
        fig.canvas.draw_idle()
        return

    def result_block(result, label, color, y_top, icon):
        if result is None:
            return y_top
        # Header bar
        bar = mpatches.FancyBboxPatch(
            (0.03, y_top-0.075), 0.94, 0.065,
            boxstyle="round,pad=0.008",
            facecolor=color, alpha=0.15,
            edgecolor=color, linewidth=0.8,
            transform=ax_res.transAxes, clip_on=False)
        ax_res.add_patch(bar)
        ax_res.text(0.07, y_top-0.042, f"{icon} {label}",
                    va="center", fontsize=8, color=color,
                    fontweight="bold", fontfamily="monospace",
                    transform=ax_res.transAxes)

        y = y_top - 0.1
        rows = [
            ("Distance",       f"{result['dist']:.0f} units"),
            ("Time",           f"{result['ms']:.2f} ms"),
        ]
        if "routes" in result:
            rows.append(("Routes checked", f"{result['routes']:,}"))
        if "comparisons" in result:
            rows.append(("Comparisons",    f"{result['comparisons']:,}"))

        for k, v in rows:
            ax_res.text(0.07, y, k,
                        va="center", fontsize=7.5, color=MUTED,
                        fontfamily="monospace",
                        transform=ax_res.transAxes)
            ax_res.text(0.93, y, v,
                        va="center", ha="right", fontsize=7.5, color=TEXT,
                        fontweight="bold", fontfamily="monospace",
                        transform=ax_res.transAxes)
            ax_res.axhline(y - 0.025, xmin=0.04, xmax=0.96,
                           color=BORDER, linewidth=0.5,
                           transform=ax_res.transAxes)
            y -= 0.07

        # Route string
        order = result["order"]
        route_str = " → ".join(cities[i]["name"] for i in order)
        route_str += " → " + cities[order[0]]["name"]
        # Wrap manually
        words = route_str.split(" → ")
        line, lines = "", []
        for w in words:
            trial = line + (" → " if line else "") + w
            if len(trial) > 28:
                lines.append(line)
                line = w
            else:
                line = trial
        if line:
            lines.append(line)

        for ln in lines[:3]:
            ax_res.text(0.07, y, ln,
                        va="center", fontsize=6.5, color=MUTED,
                        fontfamily="monospace",
                        transform=ax_res.transAxes)
            y -= 0.055

        return y - 0.04

    y = 0.87
    y = result_block(brute_route, "BRUTE FORCE",    ACCENT,  y, "⚡")
    y = result_block(heur_route,  "NEAREST NEIGHBOR", ACCENT2, y, "🧭")

    # Comparison
    if brute_route and heur_route:
        overhead = ((heur_route["dist"] - brute_route["dist"])
                    / brute_route["dist"] * 100)
        msg = (f"NN is optimal!" if overhead < 0.01
               else f"NN is {overhead:.1f}% longer than optimal")
        bar = mpatches.FancyBboxPatch(
            (0.03, y-0.06), 0.94, 0.055,
            boxstyle="round,pad=0.008",
            facecolor="#8e44ad", alpha=0.15,
            edgecolor="#8e44ad", linewidth=0.8,
            transform=ax_res.transAxes, clip_on=False)
        ax_res.add_patch(bar)
        ax_res.text(0.5, y-0.033, msg,
                    ha="center", va="center", fontsize=7.5,
                    color="#a29bfe", fontweight="bold",
                    fontfamily="monospace",
                    transform=ax_res.transAxes)

    fig.canvas.draw_idle()


def refresh():
    draw_map()
    draw_city_list()
    draw_results()
    fig.canvas.draw_idle()

# ── Interaction ────────────────────────────────────────────────────────────────

def on_click(event):
    if event.inaxes != ax_map or event.button != 1:
        return
    if len(cities) >= 10:
        ax_map.set_title("MAX 10 CITIES FOR BRUTE FORCE", color=ACCENT3,
                         fontsize=8, fontfamily="monospace")
        fig.canvas.draw_idle()
        return
    name = tb_name.text.strip() or f"City {len(cities)+1}"
    tb_name.set_val("")
    global brute_route, heur_route
    brute_route = heur_route = None
    cities.append({"name": name, "x": event.xdata, "y": event.ydata})
    refresh()

def btn_brute_cb(event):
    global brute_route, heur_route
    heur_route = None
    solve_brute()

def btn_heur_cb(event):
    global brute_route, heur_route
    brute_route = None
    solve_heuristic()

def btn_both_cb(event):
    global brute_route, heur_route
    brute_route = heur_route = None
    solve_brute()
    solve_heuristic()

def btn_preset_cb(event):
    global cities, brute_route, heur_route
    cities = [
        {"name": "Chennai",    "x": 0.15, "y": 0.25},
        {"name": "Mumbai",     "x": 0.12, "y": 0.65},
        {"name": "Delhi",      "x": 0.35, "y": 0.85},
        {"name": "Kolkata",    "x": 0.72, "y": 0.72},
        {"name": "Bangalore",  "x": 0.25, "y": 0.22},
        {"name": "Hyderabad",  "x": 0.38, "y": 0.38},
    ]
    brute_route = heur_route = None
    refresh()

def btn_reset_cb(event):
    global cities, brute_route, heur_route
    cities = []
    brute_route = heur_route = None
    refresh()

# ── Layout ─────────────────────────────────────────────────────────────────────

fig = plt.figure(figsize=(15, 8.5), facecolor=BG)
fig.suptitle("LOGISTICS ROUTE OPTIMIZER",
             fontsize=20, fontweight="bold",
             color=ACCENT, fontfamily="monospace", y=0.97)
fig.text(0.5, 0.935,
         "TRAVELLING SALESMAN PROBLEM  —  BRUTE FORCE vs NEAREST NEIGHBOR",
         ha="center", fontsize=8, color=MUTED, fontfamily="monospace")

# Axes
ax_list = fig.add_axes([0.01, 0.20, 0.15, 0.70], facecolor=CARD)
ax_map  = fig.add_axes([0.18, 0.20, 0.48, 0.70], facecolor=PANEL)
ax_res  = fig.add_axes([0.68, 0.20, 0.31, 0.70], facecolor=CARD)

for ax in (ax_list, ax_map, ax_res):
    for spine in ax.spines.values():
        spine.set_edgecolor(BORDER)
        spine.set_linewidth(1.2)

# TextBox
ax_tb = fig.add_axes([0.01, 0.12, 0.15, 0.055])
tb_name = TextBox(ax_tb, "", initial="City name…",
                  color=PANEL, hovercolor=CARD)
tb_name.label.set_fontsize(0)
tb_name.text_disp.set_color(TEXT)
tb_name.text_disp.set_fontfamily("monospace")

# Buttons
btn_defs = [
    ([0.01,  0.065, 0.072, 0.048], "⚡ BRUTE FORCE",   ACCENT,  BG,   btn_brute_cb),
    ([0.088, 0.065, 0.072, 0.048], "🧭 NEAREST NBR",   ACCENT2, BG,   btn_heur_cb),
    ([0.01,  0.015, 0.072, 0.040], "▶  SOLVE BOTH",    "#8e44ad","white", btn_both_cb),
    ([0.088, 0.015, 0.035, 0.040], "PRESET",           PANEL,   ACCENT, btn_preset_cb),
    ([0.127, 0.015, 0.033, 0.040], "RESET",            PANEL,   ACCENT3, btn_reset_cb),
]

for rect, label, bg, fg, cb in btn_defs:
    ax_b = fig.add_axes(rect)
    ax_b.set_facecolor(bg)
    for s in ax_b.spines.values():
        s.set_edgecolor(BORDER)
    btn = Button(ax_b, label, color=bg, hovercolor=CARD)
    btn.label.set_color(fg)
    btn.label.set_fontsize(8)
    btn.label.set_fontweight("bold")
    btn.label.set_fontfamily("monospace")
    btn.on_clicked(cb)
    ax_b._btn = btn

fig.canvas.mpl_connect("button_press_event", on_click)

refresh()
plt.show()
