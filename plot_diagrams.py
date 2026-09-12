#!/usr/bin/env python3
"""Plottar respektive kolumn for Landvetter.txt och VGA26.txt i samma diagram, raderna 3600-5900."""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = ["Landvetter.txt", "VGA26.txt"]
LABELS = ["Landvetter", "VGA26"]
COL_NAMES = [
    "Temp (C)",
    "Fuktighet (%)",
    "Vindriktning (deg)",
    "Vindhastighet (m/s)",
    "Nederbord (mm)",
    "Solsken (min)",
]
ROW_START = 3600
ROW_END = 5900

datasets = {}
for fname in FILES:
    path = os.path.join(HERE, fname)
    data = np.loadtxt(path, dtype=float)
    idx = data[:, 0].astype(int)
    cols = data[:, 1:]
    mask = (idx >= ROW_START) & (idx <= ROW_END)
    datasets[fname] = {"idx": idx[mask], "cols": cols[mask]}

outdir = os.path.join(HERE, "diagram")
os.makedirs(outdir, exist_ok=True)

for j, name in enumerate(COL_NAMES):
    fig, ax = plt.subplots(figsize=(12, 5))
    for fname, label in zip(FILES, LABELS):
        d = datasets[fname]
        ax.plot(d["idx"], d["cols"][:, j], linewidth=0.8, label=label)
    ax.set_title(f"{name} (rad {ROW_START}-{ROW_END})")
    ax.set_xlabel("Rad")
    ax.set_ylabel(name)
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    outpath = os.path.join(outdir, f"{j+1}_{name.split(' ')[0].lower()}.png")
    fig.savefig(outpath, dpi=120)
    plt.close(fig)
    print(f"Saved: {outpath}")

print("Klart.")
