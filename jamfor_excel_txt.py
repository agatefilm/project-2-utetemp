#!/usr/bin/env python3
"""Jamfor Excel-kolumn D och E (open-meteo) med kolumn 6 och 7 i VGA26-temp-solar.txt.

Excel-filen innehaller timdata for juni-augusti 2026.
Textfilen innehaller timdata for ett helt ar.
Skriptet hittar den tidsforshiftning dar temperaturerna overensstammer bast,
sa att Excel-rad 0 paras med motsvarande timme i textfilen, och plottar sedan:
  - Excel kolumn D (diffuse_radiation) vs textfilens kolumn 6 (solsken)
  - Excel kolumn E (direct_normal_irradiance) vs textfilens kolumn 7
i samma diagram for visuell kontroll.
"""

import os
import datetime

import numpy as np
import openpyxl
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
EXCEL = "open-meteo-57.75N11.86E14m.xlsx"
TXT = "VGA26-temp-solar.txt"

# --- Läs Excel (open-meteo): hoppa over metadata-rader, behall datarader ---
wb = openpyxl.load_workbook(os.path.join(HERE, EXCEL), read_only=True, data_only=True)
ws = wb.active
rows = list(ws.iter_rows(values_only=True))
ex = [r for r in rows if isinstance(r[0], datetime.datetime)]
ex_time = [r[0] for r in ex]
ex_temp = np.array([r[1] for r in ex], float)
ex_D = np.array([r[3] for r in ex], float)
ex_E = np.array([r[4] for r in ex], float)
n = len(ex)
ex_first = ex_time[0]
ex_last = ex_time[-1]

# --- Läs textfilen: [index, temp, fukt, vindrikt, vindhast, solsken, nederbord] ---
d = np.loadtxt(os.path.join(HERE, TXT))
text_idx = d[:, 0].astype(int)
text_temp = d[:, 1]
text_col6 = d[:, 5]
text_col7 = d[:, 6]

# --- Bestam tidsforshiftning via temperaturkorrelation ---
best_off, best_c = None, -1.0
for off in range(0, len(text_temp) - n + 1):
    seg = text_temp[off:off + n]
    if np.std(seg) == 0 or np.std(ex_temp) == 0:
        continue
    c = np.corrcoef(seg, ex_temp)[0, 1]
    if c > best_c:
        best_c, best_off = c, off

off = best_off
seg = d[off:off + n]
seg_idx = text_idx[off:off + n]
seg_col6 = seg[:, 5]
seg_col7 = seg[:, 6]

print("Excel: %s .. %s  (%d rader)" % (ex_first, ex_last, n))
print("Bast offset i textfilen: %d  (temperaturkorrelation %.3f)" % (off, best_c))
print("Text-index %d..%d paras med Excel-rad 0..%d" % (off, off + n - 1, n - 1))
print("corr text-col6 vs Excel-D(diffuse):    %.3f" % np.corrcoef(seg_col6, ex_D)[0, 1])
print("corr text-col7 vs Excel-E(direct_nor): %.3f" % np.corrcoef(seg_col7, ex_E)[0, 1])

outdir = os.path.join(HERE, "diagram_jamforelse")
os.makedirs(outdir, exist_ok=True)
x = np.arange(n)

pairs = [
    ("kolumn_D_diffuse_vs_kolumn6", ex_D, seg_col6,
     "Excel kolumn D: diffuse_radiation (W/m^2)  vs  Text kolumn 6 (solsken)"),
    ("kolumn_E_directnormal_vs_kolumn7", ex_E, seg_col7,
     "Excel kolumn E: direct_normal_irradiance (W/m^2)  vs  Text kolumn 7"),
]

for fname, excel_vals, text_vals, title in pairs:
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(x, excel_vals, linewidth=0.8, label="Excel (open-meteo)")
    ax.plot(x, text_vals, linewidth=0.8, label="VGA26-temp-solar.txt")
    ax.set_title(title)
    ax.set_xlabel("Timme (Excel-rad 0 = %s)" % ex_first.strftime("%Y-%m-%d %H:%M"))
    ax.set_ylabel("Varde")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    outpath = os.path.join(outdir, fname + ".png")
    fig.savefig(outpath, dpi=120)
    plt.close(fig)
    print("Saved: %s" % outpath)

print("Klart.")
